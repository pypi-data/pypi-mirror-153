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

import multiprocessing
import os
import copy

from PIL import Image
import keras
import numpy as np
import tensorflow as tf
from keras.callbacks import EarlyStopping, TensorBoard
from keras.layers import Reshape, Conv2D, Input, Lambda, Dropout
from keras.models import Model
from keras.optimizers import Adam

import cryolo.utils as utils
import cryolo
from cryolo.MultiGPUModelCheckpoint import MultiGPUModelCheckpoint
from cryolo.ExtendedModelCheckpoint import ExtendedModelCheckpoint
from cryolo.warmup_callback import WarmupCallback
from cryolo.SGDRSchedular import SGDRScheduler
from cryolo.backend import FullYoloFeature, CrYoloFeature, PhosaurusNetFeature, BaseFeatureExtractor
from cryolo.patchwisebatchgenerator2 import PatchwiseBatchGenerator
from cryolo.utils import BoundBox
from typing import Sequence
warmup_bs = keras.backend.variable(1.0)


class FeatureExtractorFactory():

    @staticmethod
    def create_feature_extractor(architecture : str , input_size : Sequence, input_depth : int, backend_weights : str) -> BaseFeatureExtractor:
        try:
            if architecture == "YOLO":
                return FullYoloFeature(
                    input_size, input_depth, backend_weights
                )
            elif architecture == "crYOLO":
                return CrYoloFeature(
                    input_size, input_depth, backend_weights
                )
            elif architecture == "PhosaurusNet":
                return PhosaurusNetFeature(
                    input_size, input_depth, backend_weights
                )
            else:
                raise Exception(
                    "Architecture not supported! Only support YOLO and crYOLO at the moment!"
                )
        except tf.errors.ResourceExhaustedError as e:
            print(e)
            import sys

            sys.exit(
                "Seems that crYOLO was not able to allocate memory. "
                "Is your GPU currenlty used? Check it with nivdia-smi"
            )
        return None


class YOLO:
    def __init__(
        self,
        architecture,
        input_size,
        max_box_per_image,
        anchors,
        backend_weights=None,
        uniitest=False,
        experimental_loss=False,
        pretrained_weights=None,
        pretrained_weights_init=False, #only use for pre initialization during training
        fine_tune=False,
        num_fine_tune_layers=2,
        input_depth=1,
        labels=["particle"],
        filament_model=False
    ):
        self.input_size = input_size
        self.input_depth = input_depth
        self.labels = list(labels)
        self.nb_class = len(self.labels)
        self.nb_box = int(len(anchors) / 2)
        self.class_wt = np.ones(self.nb_class, dtype="float32")
        self.anchors = anchors
        self.max_box_per_image = max_box_per_image
        self.nms_threshold = None
        self.obj_threshold = None
        self.experimental_loss = experimental_loss
        self.features = None
        self.fine_tune = fine_tune
        self.num_fine_tune_layers = num_fine_tune_layers


        ##########################
        # Make the model
        ##########################

        # make the feature extractor layers
        if not uniitest:
            if type(self.input_size) is list:
                self.input_size = self.input_size[::-1]
            else:
                self.input_size = [self.input_size,self.input_size]
            input_image = Input(
                shape=(self.input_size[1], self.input_size[0], self.input_depth),
                dtype="float32",
            )
            self.is_filament_model = filament_model
            self.true_boxes = Input(shape=(1, 1, 1, max_box_per_image, 4 + self.is_filament_model))

            self.feature_extractor = FeatureExtractorFactory.create_feature_extractor(architecture=architecture,
                                                                                      input_size=self.input_size,
                                                                                      input_depth=self.input_depth,
                                                                                      backend_weights=backend_weights)

            self.grid_rows, self.grid_columns = self.feature_extractor.get_output_shape()

            features = self.feature_extractor.extract(input_image)

            # make the object detection layer
            self.features = Dropout(0.2, name="Dropout1")(features)
            postfix = ""
            if self.is_filament_model:
                postfix = "_filament"
            output = Conv2D(
                self.nb_box * (4 + 1 + self.nb_class + self.is_filament_model),
                (1, 1),
                strides=(1, 1),
                padding="same",
                name="conv_23" + postfix,
                kernel_initializer="lecun_normal",
            )(features)
            output = Reshape(
                (self.grid_rows, self.grid_columns, self.nb_box, 4 + 1 + self.nb_class + self.is_filament_model)
            )(output)
            output = Lambda(lambda args: args[0])([output, self.true_boxes])
            self.model = Model([input_image, self.true_boxes], output)

            # initialize the weights of the detection layer
            layer = self.model.layers[-4]
            weights = layer.get_weights()

            new_kernel = np.random.normal(size=weights[0].shape) / (
                    self.grid_rows * self.grid_columns
            )
            new_bias = np.random.normal(size=weights[1].shape) / (
                    self.grid_rows * self.grid_columns
            )

            layer.set_weights([new_kernel, new_bias])

            if pretrained_weights is not None and os.path.exists(pretrained_weights):
                print("\n Load weights: ", pretrained_weights)
                self.load_weights(
                    weight_path=pretrained_weights,
                    do_fine_tune=self.fine_tune,
                    num_layers=self.num_fine_tune_layers,
                    is_init=pretrained_weights_init
                )

    def custom_loss(self, y_true, y_pred):
        """
        For y_true: The last dimension saves 6 values:
        [0]: x-position Relative to cell width. E.g.: if the cell with is 32, then the value are from 0 - 32
        [1]: y-position
        [2]: box-width In units of cell width, relative to downscaled image. E.g.: if the cell width is 25, and the
        estimataed box size 200/4=50, then it would be 2
        [3]: box-height analog to box-width
        [4]: confidence. contains 1 and 0 for y_true and -Inf to 1 for y_pred
        [5]: class-probabilites
        :param y_true: Tensor with shape [batch_size, grid_width, grid_height, num_anchor_boxes, 6]
        :param y_pred:
        :return:
        """

        mask_shape = tf.shape(y_true)[:4]

        # Generates a grid (e.g. 32 x 32) with coordinates
        cell_x = tf.to_float(
            tf.reshape(
                tf.tile(tf.range(self.grid_columns), [self.grid_rows]),
                (1, self.grid_rows, self.grid_columns, 1, 1),
            )
        )
        cell_y = tf.to_float(
            tf.reshape(tf.tile(tf.range(self.grid_rows), [self.grid_columns]), (1, self.grid_columns, self.grid_rows, 1, 1)))
        cell_y = tf.transpose(cell_y, (0, 2, 1, 3, 4))

        cell_grid = tf.tile(
            tf.concat([cell_x, cell_y], -1), [self.batch_size, 1, 1, self.nb_box, 1]
        )

        coord_mask = tf.zeros(mask_shape)
        conf_mask = tf.zeros(mask_shape)

        seen = tf.Variable(0.0)
        total_recall = tf.Variable(0.0)

        #
        # Adjust prediction
        #

        # adjust x and y
        pred_box_xy = tf.sigmoid(y_pred[..., :2]) + cell_grid #coordinate corner + relative box position

        # adjust w and h
        pred_box_wh = tf.exp(y_pred[..., 2:4]) * np.reshape(
            self.anchors, [1, 1, 1, self.nb_box, 2]
        )



        # adjust confidence
        pred_box_conf = tf.sigmoid(y_pred[..., 4])

        if self.is_filament_model:
            pred_box_angle = tf.sigmoid(y_pred[..., -1]) # from 0 to 1 -> 0 to PI
            pred_box_class = y_pred[..., 5:-1]
        else:
            # adjust class probabilities
            pred_box_class = y_pred[..., 5:]

        #
        # Adjust ground truth
        #

        # adjust x and y
        true_box_xy = y_true[..., 0:2]  # relative position to the containing cell

        # adjust w and h
        true_box_wh = y_true[
            ..., 2:4
        ]  # number of cells across, horizontally and vertically

        # adjust confidence
        true_wh_half = true_box_wh / 2.0
        true_mins = true_box_xy - true_wh_half
        true_maxes = true_box_xy + true_wh_half

        pred_wh_half = pred_box_wh / 2.0
        pred_mins = pred_box_xy - pred_wh_half
        pred_maxes = pred_box_xy + pred_wh_half

        intersect_mins = tf.maximum(pred_mins, true_mins)
        intersect_maxes = tf.minimum(pred_maxes, true_maxes)
        intersect_wh = tf.maximum(intersect_maxes - intersect_mins, 0.0)
        intersect_areas = intersect_wh[..., 0] * intersect_wh[..., 1]

        true_areas = true_box_wh[..., 0] * true_box_wh[..., 1]
        pred_areas = pred_box_wh[..., 0] * pred_box_wh[..., 1]

        union_areas = pred_areas + true_areas - intersect_areas
        iou_scores = tf.truediv(intersect_areas, union_areas)

        true_box_conf = iou_scores * y_true[..., 4]  # Page 2 in YOLO Paper

        # adjust class probabilities
        if self.is_filament_model:
            true_box_class = tf.argmax(
                y_true[..., 5:-1], -1
            )
            true_box_angle = y_true[..., -1]
        else:
            true_box_class = tf.argmax(
                y_true[..., 5:], -1
            )  # is always zero if there is only one class

        #
        # Determine the masks
        #

        # coordinate mask: simply the position of the ground truth boxes (the predictors)
        coord_mask = tf.expand_dims(y_true[..., 4], axis=-1) * self.coord_scale

        # confidence mask: penelize predictors + penalize boxes with low IOU
        # penalize the confidence of the boxes, which have IOU with some ground truth box < 0.6
        true_xy = self.true_boxes[..., 0:2]
        true_wh = self.true_boxes[..., 2:4]

        true_wh_half = true_wh / 2.0
        true_mins = true_xy - true_wh_half
        true_maxes = true_xy + true_wh_half

        pred_xy = tf.expand_dims(pred_box_xy, 4)
        pred_wh = tf.expand_dims(pred_box_wh, 4)

        pred_wh_half = pred_wh / 2.0
        pred_mins = pred_xy - pred_wh_half
        pred_maxes = pred_xy + pred_wh_half

        intersect_mins = tf.maximum(pred_mins, true_mins)
        intersect_maxes = tf.minimum(pred_maxes, true_maxes)
        intersect_wh = tf.maximum(intersect_maxes - intersect_mins, 0.0)
        intersect_areas = intersect_wh[..., 0] * intersect_wh[..., 1]

        true_areas = true_wh[..., 0] * true_wh[..., 1]
        pred_areas = pred_wh[..., 0] * pred_wh[..., 1]

        union_areas = pred_areas + true_areas - intersect_areas
        iou_scores = tf.truediv(intersect_areas, union_areas)

        best_ious = tf.reduce_max(iou_scores, axis=4)

        # penalize the confidence of the boxes, which are reponsible for corresponding ground truth box
        if self.experimental_loss:
            conf_mask_noobj = (
                conf_mask
                + tf.to_float(best_ious < 0.6)
                * (1 - y_true[..., 4])
                * self.no_object_scale
            )
            conf_mask_obj = conf_mask + y_true[..., 4] * self.object_scale
        else:
            conf_mask = (
                conf_mask
                + tf.to_float(best_ious < 0.6)
                * (1 - y_true[..., 4])
                * self.no_object_scale
            )
            conf_mask = conf_mask + y_true[..., 4] * self.object_scale

        # class mask: simply the position of the ground truth boxes (the predictors)
        class_mask = (
            y_true[..., 4] * tf.gather(self.class_wt, true_box_class) * self.class_scale
        )

        #
        # Warm-up training
        #
        no_boxes_mask = tf.to_float(coord_mask < self.coord_scale / 2.0)
        seen = tf.assign_add(seen, 1.0)

        true_box_xy, true_box_wh, coord_mask = tf.cond(
            tf.less(seen, warmup_bs),
            lambda: [
                true_box_xy + (0.5 + cell_grid) * no_boxes_mask,
                true_box_wh
                + tf.ones_like(true_box_wh)
                * np.reshape(self.anchors, [1, 1, 1, self.nb_box, 2])
                * no_boxes_mask,
                tf.ones_like(coord_mask),
            ],
            lambda: [true_box_xy, true_box_wh, coord_mask],
        )

        #
        # Finalize the loss
        #

        nb_coord_box = tf.reduce_sum(tf.to_float(coord_mask > 0.0))

        if self.experimental_loss:
            nb_conf_box_obj = tf.reduce_sum(tf.to_float(conf_mask_obj > 0.0))
            nb_conf_box_noobj = tf.reduce_sum(tf.to_float(conf_mask_noobj > 0.0))
        else:
            nb_conf_box = tf.reduce_sum(tf.to_float(conf_mask > 0.0))

        nb_class_box = tf.reduce_sum(tf.to_float(class_mask > 0.0))

        loss_xy = (
            tf.reduce_sum(tf.square(true_box_xy - pred_box_xy) * coord_mask)
            / (nb_coord_box + 1e-6)
            / 2.0
        )
        loss_wh = (
            tf.reduce_sum(tf.square(true_box_wh - pred_box_wh) * coord_mask)
            / (nb_coord_box + 1e-6)
            / 2.0
        )

        if self.is_filament_model:
            # I should do it similar to confidence, but not sure why the
            # division by 2 happens
            #loss_angle = true_box_angle - pred_box_angle
            '''
            diff_angles_a = tf.abs(true_box_angle - pred_box_angle)
            # Reason for +-0.5: The 0.5 is actuall +- PI, but the true angles are in the range from
            # 0 to 1 instead of 0 to 2PI because they are normalized. 0.5 is also actually +- PI
            diff_angles_b = tf.abs(true_box_angle - pred_box_angle + 1)
            diff_angles_c = tf.abs(true_box_angle - pred_box_angle - 1)

            diff_angles = tf.minimum(tf.math.minimum(diff_angles_a,diff_angles_b),diff_angles_c)
            '''
            dot = tf.square(
                tf.cos(true_box_angle*np.pi)*tf.cos(pred_box_angle*np.pi)+
                tf.sin(true_box_angle*np.pi)*tf.sin(pred_box_angle*np.pi)
            )
            loss_angle = (
                tf.reduce_sum((1-dot) * coord_mask[:,:,:,0,:]) # conf_mask
                / (nb_coord_box + 1e-6) # nb_conf_box
                / 2
            )


        if self.experimental_loss:
            loss_conf_obj = (
                tf.reduce_sum(tf.square(true_box_conf - pred_box_conf) * conf_mask_obj)
                / (nb_conf_box_obj + 1e-6)
                / 2.0
            )
            loss_conf_noobj = (
                tf.reduce_sum(
                    tf.square(true_box_conf - pred_box_conf) * conf_mask_noobj
                )
                / (nb_conf_box_noobj + 1e-6)
                / 2.0
            )
        else:
            loss_conf = (
                tf.reduce_sum(tf.square(true_box_conf - pred_box_conf) * conf_mask)
                / (nb_conf_box + 1e-6)
                / 2.0
            )
        loss_class = tf.nn.sparse_softmax_cross_entropy_with_logits(
            labels=true_box_class, logits=pred_box_class
        )
        loss_class = tf.reduce_sum(loss_class * class_mask) / (nb_class_box + 1e-6)

        if self.experimental_loss:
            loss = loss_xy + loss_conf_obj + loss_conf_noobj + loss_class + loss_wh
        else:
            if self.is_filament_model:
                loss = loss_xy + loss_conf + loss_class + loss_wh + loss_angle
            else:
                loss = loss_xy + loss_conf + loss_class + loss_wh

        if self.debug:
            nb_true_box = tf.reduce_sum(y_true[..., 4])
            nb_pred_box = tf.reduce_sum(
                tf.to_float(true_box_conf > 0.5) * tf.to_float(pred_box_conf > 0.3)
            )

            current_recall = nb_pred_box / (nb_true_box + 1e-6)
            total_recall = tf.assign_add(total_recall, current_recall)
            try:
                # New tensorflow > 1.10.1
                if self.experimental_loss:
                    print_op = tf.print(
                        "\n",
                        "\tLoss XY \t",
                        loss_xy,
                        "\n",
                        "\tLoss WH \t",
                        loss_wh,
                        "\n",
                        "\tLoss Obj \t",
                        loss_conf_obj,
                        "\n",
                        "\tLoss NoObj \t",
                        loss_conf_noobj,
                        "\n",
                        "\tTotal Loss \t",
                        loss,
                        "\n",
                        "\tCurrent Recall \t",
                        current_recall,
                        "\n",
                        "\tAverage Recall \t",
                        total_recall / seen,
                        "\n",
                    )
                else:
                    print_op = tf.print(
                        "\n",
                        "\tLoss XY \t",
                        loss_xy,
                        "\n",
                        "\tLoss WH \t",
                        loss_wh,
                        "\n",
                        "\tLoss Conf \t",
                        loss_conf,
                        "\n",
                        "\tLoss Angle \t",
                         loss_angle,
                        "\n",
                        "\tTotal Loss \t",
                        loss,
                        "\n",
                        "\tCurrent Recall \t",
                        current_recall,
                        "\n",
                        "\tAverage Recall \t",
                        total_recall / seen,
                        "\n",
                    )
                with tf.control_dependencies([print_op]):
                    loss = tf.identity(loss)
            except:
                # Old tensorflow == 1.10.1
                loss = tf.Print(loss, [loss_xy], message="\nLoss XY \t", summarize=1000)
                loss = tf.Print(loss, [loss_wh], message="Loss WH \t", summarize=1000)
                if self.experimental_loss:
                    loss = tf.Print(
                        loss, [loss_conf_obj], message="Loss Obj \t", summarize=1000
                    )
                    loss = tf.Print(
                        loss, [loss_conf_noobj], message="Loss NoObj \t", summarize=1000
                    )
                else:
                    loss = tf.Print(
                        loss, [loss_conf], message="Loss Conf \t", summarize=1000
                    )
                # loss = tf.Print(loss, [loss_class], message='Loss Class \t', summarize=1000)
                loss = tf.Print(loss, [loss], message="Total Loss \t", summarize=1000)
                loss = tf.Print(
                    loss, [current_recall], message="Current Recall \t", summarize=1000
                )
                loss = tf.Print(
                    loss,
                    [total_recall / seen],
                    message="Average Recall \t",
                    summarize=1000,
                )

        return loss

    def load_weights(self, weight_path: str, do_fine_tune: bool=False, num_layers: int=2, is_init: bool=False):
        '''

        :param weight_path: Path to weights
        :param do_fine_tune: Boolean flag if only fine tuning is done
        :param num_layers: Number of layers to fine tune
        :param is_init: Boolean flag. True if the weights are only loaded for pre initialization during training.
        '''

        try:
            if is_init:
                self.model.load_weights(weight_path, by_name=True)
            else:
                self.model.load_weights(weight_path)

            ###############################
            # If wanted, only train the last two layers of the network.
            ###############################
            if do_fine_tune:
                print("Do fine tuning!")
                for layer_index, layer in enumerate(self.model.layers):
                    if layer.name != "conv_23" and "model_" not in layer.name:
                        layer.trainable = False

                #
                # Find number of convolutional layers
                #
                num_conv_layers = 0

                for layer_index, layer in enumerate(
                    self.model.get_layer(index=1).layers
                ):
                    if "conv_" in layer.name:
                        num_conv_layers = num_conv_layers + 1

                #
                # Define trainable layers
                #
                free_layers = []
                for i in range(num_layers - 1):
                    layer_index = num_conv_layers - i
                    free_layers.append("conv_" + str(layer_index))
                    free_layers.append("conv_" + str(layer_index) + "_")

                #
                # Freeze other layers
                #
                for layer_index, layer in enumerate(
                    self.model.get_layer(index=1).layers
                ):
                    if layer.name not in free_layers:
                        layer.trainable = False

        except ValueError:
            ###############################
            # This is a workaround for a keras bug loading weights from nested models with fixed layers
            ###############################
            for layer_index, layer in enumerate(self.model.layers):
                if layer.name != "conv_23" and "model_" not in layer.name:
                    layer.trainable = False

            #
            # Find number of convolutional layers
            #
            num_conv_layers = 0

            for layer_index, layer in enumerate(self.model.get_layer(index=1).layers):
                if "conv_" in layer.name:
                    num_conv_layers = num_conv_layers + 1

            #
            # Define trainable layers
            #
            free_layers = []
            for i in range(num_layers - 1):
                layer_index = num_conv_layers - i
                free_layers.append("conv_" + str(layer_index))
                free_layers.append("conv_" + str(layer_index) + "_")

            #
            # Freeze other layers
            #
            for layer_index, layer in enumerate(self.model.get_layer(index=1).layers):
                if layer.name not in free_layers:
                    layer.trainable = False

                else:
                    print("Make trainable:", layer.name)

            self.model.load_weights(weight_path)

    def predict(
        self,
        image_tiles,
        tiles_coord,
        image_dimensions,
        obj_threshold=0.3,
        nms_threshold=0.3,
        num_patches=1,
        normalize_margin=0,
        normalization="STANDARD",
    ):

        self.nms_threshold = nms_threshold
        self.obj_threshold = obj_threshold
        resized_normalized_array = None
        norm_func = utils.get_normalization_func(normalization)
        for i in range(len(tiles_coord)):
            img_tmp = image_tiles[i, :, :]

            img_tmp = np.array(
                Image.fromarray(img_tmp).resize(
                    (self.input_size[0], self.input_size[1]), resample=Image.BILINEAR
                )
            )
            # cv2.resize(img_tmp, (self.input_size, self.input_size))

            if resized_normalized_array is None:
                resized_normalized_array = np.empty(
                    shape=(image_tiles.shape[0], img_tmp.shape[0], img_tmp.shape[1])
                )

            resized_normalized_array[i, :, :] = norm_func(
                img_tmp, margin_size=normalize_margin
            )

        input_image = resized_normalized_array
        input_image = np.expand_dims(input_image, 3)
        dummy_array = np.zeros(
            (input_image.shape[0], 1, 1, 1, self.max_box_per_image, 4+self.is_filament_model)
        )
        netout = self.model.predict([input_image, dummy_array])
        boxes_nms, boxes_unfiltered = self.decode_netout_fast(
            netout,
            image_tiles,
            tiles_coord,
            image_dimensions,
            obj_threshold,
            num_patches,
        )

        return boxes_nms, boxes_unfiltered

    def decode_netout_fast(
        self,
        netout_batch,
        image_tiles,
        tiles_coord,
        image_dim,
        obj_threshold=0.3,
        num_patches=1,
    ):
        nr_patches = num_patches * num_patches
        boxes_per_image = []
        boxes = []
        sigm = self.sigmoid
        for netout_index in range(netout_batch.shape[0]):
            tile_shape = image_tiles[netout_index].shape
            netout = netout_batch[netout_index, :, :, :, :]
            grid_h, grid_w, nb_box = netout.shape[:3]
            # decode the output by the network
            netout[..., 4] = sigm(netout[..., 4]) # Confidence
            if self.is_filament_model:
                netout[..., 5:-1] = netout[..., 4][..., np.newaxis] * self.softmax(
                    netout[..., 5:-1]
                )

                netout[..., 5:-1] *= netout[..., 5:-1] > min(0.1, obj_threshold)
            else:
                netout[..., 5:] = netout[..., 4][..., np.newaxis] * self.softmax(
                    netout[..., 5:]
                )

                netout[..., 5:] *= netout[..., 5:] > min(0.1, obj_threshold)

            # Transform data
            range_grid_h = np.arange(grid_h)
            range_grid_w = np.arange(grid_w)
            range_grid_w_np = np.array(range_grid_w)
            range_grid_h_np = np.array(range_grid_h)

            netout[:, :, 0, 0] = (range_grid_w_np + sigm(netout[:, :, 0, 0])) / grid_w

            netout[:, :, 0, 0] = (
                netout[:, :, 0, 0] * tile_shape[1]
                + float(tiles_coord[netout_index][0].start)
            ) / image_dim[1]

            netout[:, :, 0, 1] = (
                range_grid_h_np.reshape(range_grid_h_np.shape[0], 1)
                + sigm(netout[:, :, 0, 1])
            ) / grid_h

            netout[:, :, 0, 1] = (
                netout[:, :, 0, 1] * tile_shape[0]
                + float(tiles_coord[netout_index][1].start)
            ) / image_dim[0]

            netout[:, :, 0, 2] = (
                self.anchors[0] * np.exp(netout[:, :, 0, 2]) / grid_w
            )  # unit: image width
            netout[:, :, 0, 2] = netout[:, :, 0, 2] * tile_shape[1] / image_dim[1]

            netout[:, :, 0, 3] = (
                self.anchors[1] * np.exp(netout[:, :, 0, 3]) / grid_h
            )  # unit: image height
            netout[:, :, 0, 3] = netout[:, :, 0, 3] * tile_shape[0] / image_dim[0]

            if self.is_filament_model:
                netout[..., 6] = sigm(netout[..., 6])*np.pi

            # Create boxes data
            for row in range(grid_h):
                for col in range(grid_w):
                    for b in range(nb_box):
                        if self.is_filament_model:
                            if np.sum(netout[row, col, b, 5:-1]) > 0:
                                bb = BoundBox(
                                    x=netout[row, col, b, 0],
                                    y=netout[row, col, b, 1],
                                    w=netout[row, col, b, 2],
                                    h=netout[row, col, b, 3],
                                    c=netout[row, col, b, 4],
                                    classes=netout[row, col, b, 5:-1],
                                )
                                bb.meta={"angle":netout[row, col, b, 6]}
                                #print("Angle:", netout[row, col, b, 6])
                                boxes.append(bb)
                        else:
                            if np.sum(netout[row, col, b, 5:]) > 0:
                                bb = BoundBox(
                                        x=netout[row, col, b, 0],
                                        y=netout[row, col, b, 1],
                                        w=netout[row, col, b, 2],
                                        h=netout[row, col, b, 3],
                                        c=netout[row, col, b, 4],
                                        classes=netout[row, col, b, 5:],
                                    )
                                boxes.append(bb)
            '''
            boxes.extend(
                [
                    BoundBox(
                        x=netout[row, col, b, 0],
                        y=netout[row, col, b, 1],
                        w=netout[row, col, b, 2],
                        h=netout[row, col, b, 3],
                        c=netout[row, col, b, 4],
                        classes=netout[row, col, b, 5:],
                    )
                    for row in range(grid_h)
                    for col in range(grid_w)
                    for b in range(nb_box)
                    if np.sum(netout[row, col, b, 5:]) > 0
                ]
            )
            '''
            if (netout_index + 1) % nr_patches == 0:
                boxes_per_image.append(boxes)

                boxes = []

        boxes_nms = [
            utils.non_maxima_suppress_fast(
                boxes, self.nb_class, self.nms_threshold, min(0.1, obj_threshold)
            )
            for boxes in boxes_per_image
        ]

        boxes_thresholded = [
            [copy.deepcopy(box) for box in boxes if box.c > obj_threshold]
            for boxes in boxes_nms
        ]

        """
        for boxes in boxes_less_filtered:
            filt_box = [[box for box in boxes if box.c > obj_threshold] for boxes in boxes_less_filtered]
            boxes_nms.append(filt_box)
        """
        return boxes_thresholded, boxes_nms

    def decode_netout(
        self,
        netout_batch,
        image_tiles,
        tiles_coord,
        image_dim,
        obj_threshold=0.3,
        num_patches=1,
    ):
        nr_patches = num_patches * num_patches
        boxes_per_image = []
        boxes = []
        sigm = self.sigmoid
        for netout_index in range(netout_batch.shape[0]):

            netout = netout_batch[netout_index, :, :, :, :]
            grid_h, grid_w, nb_box = netout.shape[:3]

            # decode the output by the network
            netout[..., 4] = sigm(netout[..., 4])
            netout[..., 5:] = netout[..., 4][..., np.newaxis] * self.softmax(
                netout[..., 5:]
            )

            netout[..., 5:] *= netout[..., 5:] > min(0.01, obj_threshold)

            for row in range(grid_h):
                for col in range(grid_w):
                    for b in range(nb_box):
                        # from 4th element onwards are confidence and class classes
                        classes = netout[row, col, b, 5:]

                        if np.sum(classes) > 0:
                            # first 4 elements are x, y, w, and h
                            box_x, box_y, box_width, box_height = netout[
                                row, col, b, :4
                            ]

                            box_x = (
                                col + sigm(box_x)
                            ) / grid_w  # center position, unit: image width
                            box_y = (
                                row + sigm(box_y)
                            ) / grid_h  # center position, unit: image height

                            box_width = (
                                self.anchors[2 * b + 0] * np.exp(box_width) / grid_w
                            )  # unit: image width
                            box_height = (
                                self.anchors[2 * b + 1] * np.exp(box_height) / grid_h
                            )  # unit: image height
                            confidence = netout[row, col, b, 4]

                            box = BoundBox(
                                box_x, box_y, box_width, box_height, confidence, classes
                            )

                            tile_shape = image_tiles[netout_index].shape
                            box.x = (
                                box.x * tile_shape[1]
                                + float(tiles_coord[netout_index][0].start)
                            ) / image_dim[1]
                            box.y = (
                                box.y * tile_shape[0]
                                + float(tiles_coord[netout_index][1].start)
                            ) / image_dim[0]

                            box.w = box.w * tile_shape[1] / image_dim[1]
                            box.h = box.h * tile_shape[0] / image_dim[0]
                            boxes.append(box)
            if (netout_index + 1) % nr_patches == 0:
                boxes_per_image.append(boxes)
                boxes = []

        boxes_nms = [
            utils.non_maxima_suppress_fast(
                boxes, self.nb_class, self.nms_threshold, self.obj_threshold
            )
            for boxes in boxes_per_image
        ]

        boxes_less_filtered = [
            utils.non_maxima_suppress_fast(
                boxes, self.nb_class, self.nms_threshold, min(0.01, obj_threshold)
            )
            for boxes in boxes_per_image
        ]
        return boxes_nms, boxes_less_filtered

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def softmax(self, x, axis=-1, t=-100.0):
        x = x - np.max(x)

        if np.min(x) < t:
            x = x / np.min(x) * t

        e_x = np.exp(x)

        return e_x / e_x.sum(axis, keepdims=True)

    def train(
        self,
        train_imgs,  # the list of images to train the model
        valid_imgs,  # the list of images used to validate the model
        train_times,  # the number of time to repeat the training set, often used for small datasets
        valid_times,  # the number of times to repeat the validation set, often used for small datasets
        nb_epoch,  # number of epoches
        learning_rate,  # the learning rate
        batch_size,  # the size of the batch
        warmup_epochs,  # number of initial batches to let the model familiarize with the new dataset
        object_scale,
        no_object_scale,
        coord_scale,
        class_scale,
        cryolo_mode,
        parallel_model=None,
        saved_weights_name="best_weights.h5",
        debug=False,
        log_path="~/logs/",
        early_stop_thresh=3,
        num_patches=1,
        warm_restarts=False,
        overlap_patches=0,
        num_cpus=-1,
        do_augmentation=True,
        do_multiprocessing=True,
        normalization="STANDARD",
        filament_model=False
    ):

        self.batch_size = batch_size
        self.warmup_epochs = warmup_epochs
        global warmup_bs
        keras.backend.set_value(
            warmup_bs,
            warmup_epochs
            * (
                train_times
                * (len(train_imgs) * num_patches * num_patches / batch_size + 1)
                + valid_times
                * (len(valid_imgs) * num_patches * num_patches / batch_size + 1)
            ),
        )
        """  
        
        """
        self.object_scale = object_scale
        self.no_object_scale = no_object_scale
        self.coord_scale = coord_scale
        self.class_scale = class_scale

        self.debug = debug
        self.do_multiprocessing = do_multiprocessing

        # Create save weights path
        saved_weights_filename, saved_weights_extension = os.path.splitext(
            saved_weights_name
        )
        saved_weights_name = saved_weights_filename + "_tmp" + saved_weights_extension
        try:
            os.makedirs(os.path.dirname(saved_weights_name))
        except:
            pass

        # if warmup_epochs > 0:
        #    nb_epoch = (
        #        warmup_epochs
        #    )  # if it's warmup stage, don't train more than warmup_epochs

        ############################################
        # Compile the model
        ############################################

        optimizer = Adam(
            lr=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0
        )
        # optimizer = Nadam(lr=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
        # optimizer = SGD(lr=learning_rate, momentum=0.8, decay=0.0, nesterov=True)
        # parallel_model = multi_gpu_model(self.model,gpus=2)
        if parallel_model:
            parallel_model.compile(loss=self.custom_loss, optimizer=optimizer)
        else:
            self.model.compile(loss=self.custom_loss, optimizer=optimizer)

        ############################################
        # Make train and validation generators
        ############################################

        generator_config = {
            "IMAGE_H": self.input_size[1],
            "IMAGE_W": self.input_size[0],
            "GRID_H": self.grid_rows,
            "GRID_W": self.grid_columns,
            "BOX": self.nb_box,
            "LABELS": self.labels,
            "CLASS": len(self.labels),
            "ANCHORS": self.anchors,
            "BATCH_SIZE": self.batch_size,
            "TRUE_BOX_BUFFER": self.max_box_per_image,
            "NUM_PATCHES": num_patches,
        }

        norm_func = utils.get_normalization_func(normalization)

        patch_assignements = np.ones(shape=(num_patches, num_patches))

        train_batch = PatchwiseBatchGenerator(
            train_imgs,
            generator_config,
            patch_assignements,
            cryolo_mode=cryolo_mode,
            norm=norm_func,
            jitter=do_augmentation,
            overlap=overlap_patches,
            name="train",
            train_times=train_times,
            is_filament_training=filament_model
        )

        valid_batch = PatchwiseBatchGenerator(
            valid_imgs,
            generator_config,
            patch_assignements,
            cryolo_mode=cryolo_mode,
            norm=norm_func,
            jitter=False,
            overlap=overlap_patches,
            name="valid",
            train_times=1,
            is_filament_training=filament_model
        )

        ############################################
        # Make a few callbacks
        ############################################

        all_callbacks = []

        early_stop = EarlyStopping(
            monitor="val_loss",
            min_delta=0.001,
            patience=early_stop_thresh,
            mode="min",
            verbose=1,
        )

        if parallel_model:
            checkpoint = MultiGPUModelCheckpoint(
                saved_weights_name,
                monitor="val_loss",
                verbose=1,
                save_best_only=True,
                save_weights_only=True,
                mode="min",
                period=1,
            )
            checkpoint.set_template_model(self.model)
        else:
            checkpoint = ExtendedModelCheckpoint(
                saved_weights_name,
                monitor="val_loss",
                verbose=1,
                save_best_only=True,
                save_weights_only=True,
                mode="min",
                period=1,
            )
        checkpoint.set_anchors(self.anchors)
        checkpoint.set_fine_tune(self.fine_tune, self.num_fine_tune_layers)
        checkpoint.set_version(cryolo.__version__)
        checkpoint.set_filamet_model(self.is_filament_model)

        reduceLROnPlateau = keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.1,
            patience=int(early_stop_thresh * 0.6),
            verbose=1,
        )

        warmup_callback = WarmupCallback(
            warmup_bs=warmup_bs,
            num_warmup_epochs=warmup_epochs,
            len_train_img=len(train_imgs),
            len_valid_img=len(valid_imgs),
            batch_size=self.batch_size,
            num_patches=num_patches,
            train_times=train_times,
            valid_times=valid_times,
            early_stop_callback=early_stop,
            modelcheckpoint=checkpoint,
            reduceonnplateau=reduceLROnPlateau,
        )

        ##APPEND CALLBACKS

        all_callbacks.append(early_stop)
        all_callbacks.append(checkpoint)
        if not warm_restarts:
            all_callbacks.append(reduceLROnPlateau)

        tb_counter = (
            len(
                [
                    log
                    for log in os.listdir(os.path.expanduser(log_path))
                    if "yolo" in log
                ]
            )
            + 1
        )
        tensorboard = TensorBoard(
            log_dir=os.path.expanduser(log_path) + "yolo" + "_" + str(tb_counter),
            histogram_freq=0,
            write_graph=True,
            write_images=False,
        )
        all_callbacks.append(tensorboard)
        all_callbacks.append(warmup_callback)
        schedule = SGDRScheduler(
            min_lr=1e-7,
            max_lr=1e-4,
            steps_per_epoch=len(train_batch),
            lr_decay=0.9,
            cycle_length=5,
            mult_factor=1.5,
        )
        if warm_restarts:
            all_callbacks.append(schedule)

        num_workers = multiprocessing.cpu_count() // 2
        if num_cpus != -1:
            num_workers = num_cpus
        #self.use_multiprocessing=False
        num_workers = 1
        ############################################
        # Start the training process
        ############################################
        if parallel_model:
            parallel_model.fit_generator(
                generator=train_batch,
                steps_per_epoch=len(train_batch),
                epochs=nb_epoch,
                verbose=1,
                validation_data=valid_batch,
                validation_steps=len(valid_batch),
                callbacks=all_callbacks,
                workers=num_workers,
                max_queue_size=multiprocessing.cpu_count(),
                use_multiprocessing=self.do_multiprocessing,
            )
        else:
            self.model.fit_generator(
                generator=train_batch,
                steps_per_epoch=len(train_batch),
                epochs=nb_epoch,
                verbose=1,
                validation_data=valid_batch,
                validation_steps=len(valid_batch),
                callbacks=all_callbacks,
                workers=num_workers,
                max_queue_size=multiprocessing.cpu_count(),
                use_multiprocessing=self.do_multiprocessing,
            )
        # Rename to the user specified filename
        if os.path.exists(saved_weights_name):
            os.rename(saved_weights_name, saved_weights_filename + saved_weights_extension)
