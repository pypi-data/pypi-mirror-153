#
# COPYRIGHT
#
# All contributions by Ngoc Anh Huyn:
# Copyright (c) 2017, Ngoc Anh Huyn.
# All rights reserved.
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
import copy
import multiprocessing as mp
import random
import time
from PIL import Image
import cryolo.utils as utils

import numpy as np
from keras.utils import Sequence

import cryolo.imagereader as imagereader
from cryolo.augmentation.augmentation import Augmentation
from cryolo.augmentation.FlipAugmentation import FlipAugmentation
from cryolo.augmentation.CustomRotationAugmentation import CustomRotationAugmentation
from cryolo.augmentation.Rot90Augmentation import Rot90Augmentation
from cryolo.utils import BoundBox, bbox_iou


class PatchwiseBatchGenerator(Sequence):
    def __init__(
        self,
        images,
        config,
        patch_assigments,
        cryolo_mode,
        shuffle=True,
        jitter=True,
        norm=None,
        overlap=100,
        name=None,
        train_times=1,
        is_filament_training=False
    ):
        self.is_filament_training=is_filament_training
        self.myname = name
        self.images = images
        self.imgdepth = 3
        self.config = config
        self.shuffle = shuffle
        self.jitter = jitter
        self.cryolo_mode = cryolo_mode
        self.norm = norm
        self.patch_assigments = patch_assigments
        self.overlap = overlap
        self.anchors = [
            BoundBox(0, 0, config["ANCHORS"][2 * i], config["ANCHORS"][2 * i + 1])
            for i in range(int(len(config["ANCHORS"]) // 2))
        ]
        self.train_times = train_times

        self.lock = mp.Lock()
        self.batch_size = self.config["BATCH_SIZE"]
        img_first = imagereader.image_read(self.images[0]["filename"])

        # Generate all coordinates:
        self.patch_coords = []
        for i in range(len(images)):
            for p_x in range(config["NUM_PATCHES"]):
                for p_y in range(config["NUM_PATCHES"]):
                    self.patch_coords.extend([(i, p_x, p_y)] * train_times)

        random.shuffle(self.patch_coords)

        if len(img_first.shape) == 2:
            self.imgdepth = 1
        elif img_first.shape[0] == 3 and np.all(
                img_first[:, :, 0] == img_first[:, :, 1]) and np.all(
                img_first[:, :, 0] == img_first[:, :, 2]
                ):
            self.imgdepth = 1
        elif len(img_first.shape) == 3 and img_first.shape[0] > 3:
            # Tomo data
            self.imgdepth = 1


    def __len__(self):
        length = int(np.ceil(len(self.patch_coords) / self.batch_size))
        return length

    def __getitem__(self, idx):
        np.random.seed()
        if ((idx + 1) * self.batch_size) > len(self.patch_coords):
            coords = self.patch_coords[idx * self.batch_size :]
            while len(coords) != self.batch_size:
                num_missing_elements = self.batch_size - len(coords)
                coords.extend(self.patch_coords[:num_missing_elements])
        else:
            coords = self.patch_coords[
                idx * self.batch_size : (idx + 1) * self.batch_size
            ]
        x_batch = np.zeros(
            (
                self.batch_size,
                self.config["IMAGE_H"],
                self.config["IMAGE_W"],
                self.imgdepth,
            ),
            dtype=np.float32,
        )  # input images
        b_batch = np.zeros(
            (self.batch_size, 1, 1, 1, self.config["TRUE_BOX_BUFFER"], 4 + self.is_filament_training),
            dtype=np.float32,
        )  # list of self.config['TRUE_self.config['BOX']_BUFFER'] GT boxes
        y_batch = np.zeros(
            (
                self.batch_size,
                self.config["GRID_H"],
                self.config["GRID_W"],
                self.config["BOX"],
                4 + self.is_filament_training + 1 + self.config["CLASS"],
            ),
            dtype=np.float32,
        )  # desired network output
        aug_times = []
        if len(coords) != self.batch_size:
            import sys

            print(
                "PATCHCOORDS",
                len(self.patch_coords),
                "LEN_COORDS:",
                len(coords),
                "BATCHSIZE:",
                self.batch_size,
                "MIN",
                num_missing_elements,
            )
            sys.exit("Error while batch creation")

        for sample_index, patch in enumerate(coords):

            # If no unselected patches are available but still intances left then reset patch_assigments_3d
            # print np.sum(np.nonzero(self.patch_assigments_3d[:, :, ]))
            img_index = patch[0]
            patch_x = patch[1]
            patch_y = patch[2]

            tile = None
            if self.config["NUM_PATCHES"] > 1:
                imgw, imgh = imagereader.read_width_height(
                    self.images[img_index]["filename"]
                )

                tile = imagereader.get_tile_coordinates(
                    imgw=imgw,
                    imgh=imgh,
                    num_patches=self.config["NUM_PATCHES"],
                    patchxy=(patch_x, patch_y),
                    overlap=self.overlap,
                )
            # Apply augmentation
            start_aug = time.time()
            # print("Filter_width:", filter_width)
            img, all_objs = self.aug_image(
                self.images[img_index], jitter=self.jitter, region=tile
            )
            end_aug = time.time()
            aug_times.append(end_aug - start_aug)

            if self.imgdepth == 1:
                img = img[:, :, np.newaxis]

            # Add to training batch
            true_box_index = 0
            for obj in all_objs:

                if (
                    obj["xmax"] > obj["xmin"]
                    and obj["ymax"] > obj["ymin"]
                    and obj["name"] in self.config["LABELS"]
                ):
                    center_x = 0.5 * (obj["xmin"] + obj["xmax"])
                    center_y = 0.5 * (obj["ymin"] + obj["ymax"])
                    # print "x ", center_x, " y ", center_y
                    center_x = center_x / (
                        float(self.config["IMAGE_W"]) / self.config["GRID_W"]
                    )
                    center_y = center_y / (
                        float(self.config["IMAGE_H"]) / self.config["GRID_H"]
                    )

                    grid_x = int(np.floor(center_x))
                    grid_y = int(np.floor(center_y))

                    if (
                        grid_x < self.config["GRID_W"]
                        and grid_y < self.config["GRID_H"]
                    ):
                        obj_indx = self.config["LABELS"].index(obj["name"])

                        center_w = (obj["xmax"] - obj["xmin"]) / (
                            float(self.config["IMAGE_W"]) / self.config["GRID_W"]
                        )  # unit: grid cell
                        center_h = (obj["ymax"] - obj["ymin"]) / (
                            float(self.config["IMAGE_H"]) / self.config["GRID_H"]
                        )  # unit: grid cell

                        if self.is_filament_training:
                            angle = obj["angle"] / np.pi # normalize it between 0 and 1
                            box = [center_x, center_y, center_w, center_h, angle]
                        else:
                            box = [center_x, center_y, center_w, center_h]

                        # find the anchor that best predicts this box
                        best_anchor = -1
                        max_iou = -1

                        shifted_box = BoundBox(0, 0, center_w, center_h)

                        for i in range(len(self.anchors)):
                            anchor = self.anchors[i]
                            iou = bbox_iou(shifted_box, anchor)

                            if max_iou < iou:
                                best_anchor = i
                                max_iou = iou

                        # assign ground truth x, y, w, h, confidence and class probs to y_batch

                        y_batch[sample_index, grid_y, grid_x, best_anchor, 0:4] = box[0:4]
                        y_batch[sample_index, grid_y, grid_x, best_anchor, 4] = 1.0
                        y_batch[
                            sample_index, grid_y, grid_x, best_anchor, 5 + obj_indx
                        ] = 1
                        if self.is_filament_training:
                            y_batch[
                                sample_index, grid_y, grid_x, best_anchor, 5 + obj_indx + 1
                            ] = angle # this line will lead to problems when multiple classes
                            # would be predicted, as obj_indx then might be > 0

                        # assign the true box to b_batch
                        b_batch[sample_index, 0, 0, 0, true_box_index] = box

                        true_box_index += 1
                        true_box_index = true_box_index % self.config["TRUE_BOX_BUFFER"]

            # assign input image to x_batch
            if self.norm is not None:
                x_batch[sample_index] = self.norm(img)

        return [x_batch, b_batch], y_batch

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.patch_coords)

    def aug_image(self, train_instance, jitter, region=None):


        def resize(image,shape,copy=False):
            image = np.array(
                Image.fromarray(image).resize(
                    shape,
                    resample=Image.BILINEAR,
                ),
                copy=copy
            )

            return image

        if "filename_filtered" in train_instance:
            image_name = train_instance["filename_filtered"]
        else:
            image_name = train_instance["filename"]
        patch_mode = region is not None
        if "z" in train_instance:
            # Get correct slice in case of tomograms
            image = imagereader.image_read(image_name, region, use_mmap=True)
            image = image[int(train_instance["z"]),:,:]
        else:
            image = imagereader.image_read(image_name, region, use_mmap=False)
        h = image.shape[0]
        w = image.shape[1]

        # if the filtered image size is not equals the input image size
        # that means we are in mixed-size mode. Set region randomly
        if self.cryolo_mode == utils.CryoloMode.MIXED_ASPECT_RATIO:
            diffh = h - self.config["IMAGE_H"]
            diffw = w - self.config["IMAGE_W"]
            if diffh > 0.0:
                starth = np.random.randint(0, diffh)
            else:
                starth = 0
            if diffw > 0.0:
                startw = np.random.randint(0, diffw)
            else:
                startw = 0
            endh = starth+self.config["IMAGE_H"]
            endw = startw+self.config["IMAGE_W"]
            region = np.s_[starth:endh, startw:endw]
            image = image[region]

            # Format region into original coordinates
            original_width, original_height = train_instance["img_size"]
            endh_scaled = endh*original_height/h
            starth_scaled = starth*original_height/h

            endw_scaled = endw * original_width / w
            startw_scaled = startw * original_width / w
            region = np.s_[starth_scaled:endh_scaled, startw_scaled:endw_scaled]

            # w and h have to be updated now!
            w = endw-startw
            h = endh-starth

        all_objs = copy.deepcopy(train_instance["object"])

        if jitter:
            # scale the image

            scale = np.random.uniform() / 10.0 + 1.0
            image = resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)), copy=True)

            # translate the image
            max_offx = (scale - 1.0) * w
            max_offy = (scale - 1.0) * h
            offx = int(np.random.uniform() * max_offx)
            offy = int(np.random.uniform() * max_offy)

            image = image[offy : (offy + h), offx : (offx + w)]

            image = resize(image, (self.config["IMAGE_W"], self.config["IMAGE_H"]),copy=True)


            # flip the image

            flip_selection = np.random.randint(0, 4)
            aug_flip = FlipAugmentation(flipping_mode=flip_selection)
            image = aug_flip.transform_image(image)


            if image.shape[0] == image.shape[1]:
                num_rots = np.random.randint(4)
            else:
                num_rots = np.random.choice([2,4])
            aug_rot = Rot90Augmentation(num_rotations=num_rots)
            image = aug_rot.transform_image(image=image)



            # rotation random degree maybe here?
            custom_rotation = np.random.rand()>0.5
            if custom_rotation:
                custom_rotation_angle = np.random.rand() * np.pi/4
                custrot = CustomRotationAugmentation(custom_rotation_angle)
                image = custrot.transform_image(image)

            is_grey = np.issubdtype(image.dtype, np.int8) or np.issubdtype(
                image.dtype, np.uint8
            )

            aug = Augmentation(is_grey)
            image = aug.image_augmentation(image)

        # resize the image to standard size
        if not jitter:
            image = resize(image, (self.config["IMAGE_W"], self.config["IMAGE_H"]), copy=True)

        if self.imgdepth == 3:
            image = image[:, :, ::-1]

        # fix objects's position and size and check region
        obj_is_region = []
        original_width, original_height = train_instance["img_size"]
        if (
            int(original_width - w) != 0 or int(original_height - h) != 0
        ) and patch_mode is False:
            # In case of "fast filtering", we need the original image size here
            w = original_width
            h = original_height
            if region is not None:
                # In case of mixed-sizes  we have to set it to the size of the original cut-off region...
                w = region[1].stop - region[1].start
                h = region[0].stop - region[0].start
            if jitter:
                offx = offx * w / float(self.config["IMAGE_W"])
                offy = offy * h / float(self.config["IMAGE_H"])

        for obj in all_objs:
            if region is None:
                is_in_region = True
            else:
                bwidth = obj["xmax"] - obj["xmin"]
                bheight = obj["ymax"] - obj["ymin"]
                obj_center_x = int(obj["xmax"] - bwidth / 2)
                obj_center_y = int(obj["ymax"] - bheight / 2)
                region_x_start = int(region[0].start + (bwidth / 2) * 0.9)
                region_x_stop = int(region[0].stop - (bwidth / 2) * 0.9)
                region_y_start = int(region[1].start + (bheight / 2) * 0.9)
                region_y_stop = int(region[1].stop - (bheight / 2) * 0.9)

                is_in_region = obj_center_x in range(
                    region_x_start, region_x_stop
                ) and obj_center_y in range(region_y_start, region_y_stop)

            if is_in_region:

                region_off_x = 0
                region_off_y = 0

                if region is not None:
                    region_off_x = region[1].start  # * w/float(self.config["IMAGE_W"])
                    region_off_y = region[0].start  # * h/float(self.config["IMAGE_H"])

                for attr in ["xmin", "xmax"]:
                    obj[attr] = obj[attr] - region_off_x
                    if jitter:
                        obj[attr] = obj[attr] * scale - offx
                    obj[attr] = obj[attr] * float(self.config["IMAGE_W"]) / w
                    obj[attr] = max(min(obj[attr], self.config["IMAGE_W"]), 0)

                for attr in ["ymin", "ymax"]:
                    obj[attr] = obj[attr] - region_off_y
                    if jitter:
                        obj[attr] = obj[attr] * scale - offy
                    obj[attr] = obj[attr] * float(self.config["IMAGE_H"]) / h
                    obj[attr] = max(min(obj[attr], self.config["IMAGE_H"]), 0)

                if jitter and aug_flip:
                    obj = aug_flip.transform_coords([obj], [self.config["IMAGE_W"],self.config["IMAGE_H"]])[0]

                if jitter and num_rots > 0:
                    obj = aug_rot.transform_coords([obj], [self.config["IMAGE_W"],self.config["IMAGE_H"]])[0]

                if jitter and custom_rotation:
                    obj = custrot.transform_coords([obj], image_dims=[self.config["IMAGE_W"], self.config["IMAGE_H"]])[0]
                    centerx = obj["xmin"] + (obj["xmax"] - obj["xmin"]) / 2
                    centery = obj["ymin"] + (obj["ymax"] - obj["ymin"]) / 2

                    if centerx < 0 or centerx>self.config["IMAGE_W"] or centery < 0 or centery>self.config["IMAGE_H"]:
                        continue

                obj_is_region.append(obj)
        #print(image.dtype)
        if False:

            print(image_name, int(train_instance["z"]), len(all_objs), len(obj_is_region))
            if len(obj_is_region)>0:
                for kk in range(len(obj_is_region)):
                    print(obj_is_region[kk])
        return image, obj_is_region
