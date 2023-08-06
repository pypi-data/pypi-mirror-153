#
# COPYRIGHT
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
import imageio
import mrcfile
import numpy as np
from PIL import Image


def image_read(image_path, region=None,use_mmap=False):
    image_path = str(image_path)
    if image_path.endswith(("jpg", "png")):
        if not is_single_channel(image_path):
            raise Exception("Not supported image format. Movie files are not supported")
            return None
        img = imageio.imread(image_path, pilmode="L", as_gray=True)
        img = img.astype(np.uint8)
    elif image_path.endswith(("tiff", "tif")):
        img = imageio.imread(image_path)
    # img = np.flipud(img)
    elif image_path.endswith(("mrc", "mrcs", "rec")):
        img = read_mrc(image_path,use_mmap)
    else:
        raise Exception("Not supported image format: " + image_path)

    # OpenCV has problems with some datatypes
    if np.issubdtype(img.dtype, np.uint32):
        img = img.astype(dtype=np.float64)

    if np.issubdtype(img.dtype, np.float16):
        img = img.astype(dtype=np.float32)

    if np.issubdtype(img.dtype, np.uint16):
        img = img.astype(dtype=np.float32)

    if region is not None:
        return img[region[1], region[0]]
    return img


def image_write(image_path, image):
    if image_path.endswith(("jpg", "png")):
        imageio.imwrite(image_path, image)
    elif image_path.endswith(("tiff", "tif")):
        if len(image.shape) == 3 and image.shape[0]>1:
            raise NotImplementedError("Only support mrc/mrcs for volume data.")
        image = np.float32(image)
        image = np.squeeze(image)
        imageio.imwrite(image_path, image)
    elif image_path.endswith(("mrc", "mrcs", "rec")):
        if len(image.shape) == 3:
            #image = np.flip(image, axis=0) # Maybe this?
            image = np.flip(image, axis=1)
        else:
            image = np.flipud(image)
        with mrcfile.new(image_path, overwrite=True) as mrc:
            mrc.set_data(np.float32(image))


def is_single_channel(image_path):
    if image_path.endswith(("jpg", "png", "tiff", "tif")):
        im = Image.open(image_path)
        if len(im.size) > 2:
            return False

    if image_path.endswith(("mrc", "mrcs", "rec")):
        with mrcfile.mmap(image_path, permissive=True, mode="r") as mrc:
            if mrc.header.nz > 1:
                return False

    return True

def get_num_frames(image_path, channel_index = 0):
    if image_path.endswith(("jpg", "png", "tiff", "tif")):
        im = Image.open(image_path)
        if len(im.size) == 2:
            return 1
        if len(im.size) == 3:
            return im.size[channel_index]

    if image_path.endswith(("mrc", "mrcs", "rec")):
        with mrcfile.mmap(image_path, permissive=True, mode="r") as mrc:
            if len(mrc.data.shape) == 2:
                return 1
            if len(mrc.data.shape) == 3:
                return mrc.data.shape[channel_index]




def read_width_height(image_path):
    if image_path.endswith(("jpg", "png", "tiff", "tif")):
        im = Image.open(image_path)
        width, height = [int(i) for i in im.size]
        return width, height

    if image_path.endswith(("mrc", "mrcs", "rec")):
        with mrcfile.mmap(image_path, permissive=True, mode="r") as mrc:
            img_height = mrc.header.ny
            img_width = mrc.header.nx
        return img_width, img_height


def read_mrc(image_path, use_mmap=False):

    if use_mmap:
        with mrcfile.mmap(image_path, permissive=True, mode="r") as mrc:
            mrc_image_data = mrc.data
    else:
        mrc_image_data = mrcfile.open(image_path, permissive=True, mode='r')
        mrc_image_data = mrc_image_data.data
    mrc_image_data = np.squeeze(mrc_image_data)
    if len(mrc_image_data.shape)==3: #Maybe this to fix it with tomograms?
        mrc_image_data = np.flip(mrc_image_data, 1)
        #mrc_image_data = np.flip(mrc_image_data, 0)
    else:
        mrc_image_data = np.flipud(mrc_image_data) # this will not work for tomograms...
    return mrc_image_data


def get_tile_coordinates(imgw, imgh, num_patches, patchxy, overlap=0):
    patch_width = int(imgw / num_patches)
    patch_height = int(imgh / num_patches)
    region_from_x = int(patchxy[0] * patch_width)
    region_to_x = int((patchxy[0] + 1) * patch_width)
    region_from_y = int(patchxy[1] * patch_height)
    region_to_y = int((patchxy[1] + 1) * patch_height)
    overlap = int(overlap)
    if patchxy[0] == 0:
        region_to_x = region_to_x + 2 * overlap
    elif patchxy[0] == (num_patches - 1):
        region_from_x = region_from_x - 2 * overlap
    else:
        region_from_x = region_from_x - overlap
        region_to_x = region_to_x + overlap

    if patchxy[1] == 0:
        region_to_y = region_to_y + 2 * overlap
    elif patchxy[1] == (num_patches - 1):
        region_from_y = region_from_y - 2 * overlap
    else:
        region_from_y = region_from_y - overlap
        region_to_y = region_to_y + overlap

    if region_to_x > imgw:
        region_to_x = imgw
    if region_to_y > imgh:
        region_to_y = imgh

    tile = np.s_[region_from_x:region_to_x, region_from_y:region_to_y]

    return tile
