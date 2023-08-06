#
# COPYRIGHT
#
# All contributions by Thorsten Wagner:
# Copyright (c) 2017 - 2019, Thorsten Wagner.
# All rights reserved.
#
# ---------------------------------------------------------------------------
#         Do not reproduce or redistribute, in whole or in part.
#      Use of this code is permitted only under licence from Max Planck Society.
#            Contact us at thorsten.wagner@mpi-dortmund.mpg.de
# ---------------------------------------------------------------------------
#
import multiprocessing
import os
import warnings

import numpy as np
import scipy.fftpack as fft

import cryolo.imagereader as imagereader

def window(width, shape):
    """

    :param image:
    :param width: Width of the gaussian filter in fourier pixel
    :return:
    """
    center_image_y = shape[0] / 2
    center_image_x = shape[1] / 2
    x_coord_vec = np.linspace(0, shape[1], shape[1])
    y_coord_vec = np.linspace(0, shape[0], shape[0])
    x_coord_mat, y_coord_mat = np.meshgrid(x_coord_vec, y_coord_vec, sparse=True)
    sq1 = ((y_coord_mat - center_image_y) ** 2)
    sq2 = ((x_coord_mat - center_image_x) ** 2)
    sqs = sq1 + sq2

    sq = np.sqrt(
            sqs
        )
    dist_mat = np.float16(
        sq
        + width / 2
    )
    gmask = np.sin(np.pi * dist_mat / (width - 1))
    gmask[dist_mat > width] = 0
    return gmask


def next_power_of2(number):
    return int(np.power(2, np.ceil(np.log2(number))))


def zero_pad(img, size_new):
    pad_extends = []
    dif_shape_y = size_new[0] - img.shape[0]
    dif_shape_x = size_new[1] - img.shape[1]

    pad_extends.append((dif_shape_y // 2, dif_shape_y // 2 + dif_shape_y % 2))
    pad_extends.append((dif_shape_x // 2, dif_shape_x // 2 + dif_shape_x % 2))

    padded = np.pad(img, pad_extends, "symmetric")

    return padded, pad_extends


def apply_fft_mask(img, mask):
    """
    Filter your image with a mask
    :param img: Image to be filtered (numpy array)
    :param mask: Mask you want to apply in fft space
    :return: Return filtered image
    """
    input_image_shape = img.shape

    # Zero Pad
    new_image_size = mask.shape
    padded, pad_extends = zero_pad(img, new_image_size)

    # The input image is not needed anymore at this point
    del img

    # FFT
    img_fft = fft.fft2(padded)

    # Padded image is not needed anymore
    del padded

    img_fft = fft.fftshift(img_fft)
    # Windowing with cosine window

    img_fft_windowed = img_fft * mask
    del img_fft

    # Backward fft
    img_fft_windowed = fft.ifftshift(img_fft_windowed)
    img_filtered = fft.ifft2(img_fft_windowed)

    del img_fft_windowed
    # Crop
    img_cropped = img_filtered[
        pad_extends[0][0] : (pad_extends[0][0] + input_image_shape[0]),
        pad_extends[1][0] : (pad_extends[1][0] + input_image_shape[1]),
    ]

    del img_filtered

    return np.real(img_cropped)


def filter_images(images, filter_cutoff, filter_tmp_path, num_cpu=-1, resize_to_shape=None):
    """
    Function will filter images gives in the image dictonary, write them into the filter_output_path

    :param images: list of images
    :param filter_cutoff: Absolute cutoff frequence (0-0.5)
    :param filter_tmp_path: Output directory for temporary files
    :return: None
    """

    if not os.path.isdir(filter_tmp_path):
        os.makedirs(filter_tmp_path)

    # Correct absolute filenames
    adapted_paths = [
        img["filename"][1:] if img["filename"][0] == "/" else img["filename"]
        for img in images
    ]

    # Create file paths for filtered files
    filtered_file_paths = [
        os.path.join(filter_tmp_path, img_pth) for img_pth in adapted_paths
    ]


    # Get index of images that are already filtered
    index_images_already_filtered = [i for i,file in enumerate(filtered_file_paths) if os.path.exists(file)]

    # Updates paths for already filtered images
    for index in index_images_already_filtered:
        images[index]["filename"] = filtered_file_paths[index]

    # Update paths that are double
    unique_paths = []
    unique_indices = []

    for image_index, path in enumerate(filtered_file_paths):
        if path not in unique_paths:
            unique_paths.append(path)
            unique_indices.append(image_index)
        else:
            images[image_index]["filename"] = filtered_file_paths[image_index]

    # Get index of images that have to be filtered
    index_images_to_filter = [
        i
        for i, pth in enumerate(filtered_file_paths)
        if not os.path.exists(pth) and
           os.path.basename(pth)[0] != "." and i in unique_indices
    ]


    # Create argument tubles for them
    arg_tubles = []
    arg_tubles.extend(
        [
            (images[i]["filename"], filter_cutoff, filter_tmp_path, -1, -1, resize_to_shape)
            for i in index_images_to_filter
        ]
    )

    # Do the filtering
    num_processes = None
    if num_cpu > 0:
        num_processes = num_cpu

    pool = multiprocessing.Pool(
        maxtasksperchild=1, processes=num_processes
    )
    all_filtered_images_paths = pool.starmap(
        filter_single_image_and_write_to_disk, arg_tubles, chunksize=1
    )
    pool.close()
    pool.join()

    # Update paths of newly filtered images
    for i, index in enumerate(index_images_to_filter):
        images[index]["filename"] = all_filtered_images_paths[i]


def filter_single_image_and_write_to_disk(
    img_path,
    filter_cutoff,
    output_path_filtered_images,
    img_num=-1,
    total_num=-1,
    resize_to_shape=None,
):
    """
    Filteres the image in img_path, save it to disk and returns the path to the filtered images
    :param img_path: Path to image to filter
    :param filter_cutoff: Absolute frequence (0 - 0.5)
    :param output_path_filtered_images: Output path for filtered images
    :param resize_to_shape: tuple with image size. the image will be downsized to this size before filtering
    :return: Path to the filtered image
    """
    dirname = os.path.dirname(img_path)
    if dirname.startswith("/"):
        dirname = dirname[1:]
    filtered_image_folder = os.path.join(output_path_filtered_images, dirname)
    filtered_img_tmp_file_path = os.path.join(
        filtered_image_folder, os.path.basename(img_path)
    )
    if not os.path.exists(filtered_img_tmp_file_path):
        if filter_cutoff > 0.5:
            warnings.simplefilter("once", UserWarning)
            print("Filter cutoff has to be smaller than 0.5. Set it to 0.5")
            filter_cutoff = 0.5

        os.makedirs(filtered_image_folder, exist_ok=True)
        if img_num != -1 and total_num != -1:
            print(
                "Filtering ",
                img_path,
                "( Progress:",
                int(img_num / total_num * 100),
                "% )",
            )
        else:
            print("Filtering ", img_path)

        image_filtered = filter_single_image(
            img_path=img_path, filter_cutoff=filter_cutoff, resize_to_shape=resize_to_shape
        )
        if image_filtered is None:
            return None
        imagereader.image_write(filtered_img_tmp_file_path, image_filtered)
        del image_filtered
    return filtered_img_tmp_file_path


def filter_single_image_from_np_array(image, filter_cutoff, resize_to_shape=None, channel_specifiction=0):
    """
    Given an image as numpy array, this procedure resize it optionally to a target size and then applies
    an low-pass filter on the image.

    :param image: Image/tomogram as numpy array
    :param filter_cutoff: Absolute frequency cutoff
    :param resize_to_shape: (Optional) Resize the image after filtering
    :param channel_specification: 0 for channel first, -1 for channel last (default is 0)
    :return: Filtered numpy arraz
    """

    cutoff_factor = 1.0
    if resize_to_shape is not None:
        if not isinstance(resize_to_shape, (list, tuple)):
            'Scale the short side to 1024'
            #         h              w
            ar = image.shape[0] / image.shape[1]
            if len(image.shape)>2:
                if channel_specifiction == 0:
                    ar = image.shape[1] / image.shape[2]
            if ar < 1:
                height = resize_to_shape
                width = int(resize_to_shape / ar)
            else:
                height = int(resize_to_shape * ar)
                width = resize_to_shape
            resize_to_shape = [height, width]
    if len(image.shape) == 2:
        if channel_specifiction == 0:
            image = image[np.newaxis, ...]
        else:
            image = image[..., np.newaxis]



    # Do filtering
    mask = None
    image_filtered_result = None
    for i in range(image.shape[channel_specifiction]):
        if channel_specifiction == 0:
            img = image[i]
        else:
            img = image[:,:,i]

        if resize_to_shape is not None:
            cutoff_factor = img.shape[0] / resize_to_shape[0]
            from PIL import Image
            convert_to_array = Image.fromarray(img)
            resized = convert_to_array.resize((resize_to_shape[1], resize_to_shape[0]),
                                              resample=Image.BILINEAR)
            img = np.asarray(resized)
        if image_filtered_result is None:
            if channel_specifiction == 0:
                image_filtered_result = np.zeros(
                    shape=(image.shape[channel_specifiction],img.shape[0],img.shape[1]),
                )
            else:
                image_filtered_result = np.zeros(
                    shape=(img.shape[0], img.shape[1],image.shape[channel_specifiction]),
                )
        mask_size_0 = next_power_of2(img.shape[0])
        mask_size_1 = next_power_of2(img.shape[1])
        filter_width = 2 * img.shape[1] * filter_cutoff * cutoff_factor
        if mask is None:
            mask = window(filter_width, (mask_size_0, mask_size_1))
        image_filtered = apply_fft_mask(img, mask)
        if channel_specifiction == 0:
            image_filtered_result[i] = image_filtered
        else:
            image_filtered_result[:, :, i] = image_filtered
        del img
        #image_filtered_result = np.squeeze(image_filtered_result)

    return image_filtered_result

def filter_single_image(img_path, filter_cutoff, resize_to_shape=None):
    """
    This procedure reads an abitary image, resize it optionally to a target size then apply
    an low-pass filter on the image.

    :param img_path: Path to the image/tomogram to be filtered
    :param filter_cutoff: Absolute frequency cutoff
    :param resize_to_shape: (Optional) Resize the image after filtering
    :return: Filtered and resized image/tomogram
    """

    try:
        image = imagereader.image_read(img_path)
    except Exception:
        print(img_path + " is corrupted. Ignore it.")
        return None
    return filter_single_image_from_np_array(image, filter_cutoff, resize_to_shape)

