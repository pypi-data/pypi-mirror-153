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

import os
from keras.layers import (
    Conv2D,
    Input,
    MaxPooling2D,
    BatchNormalization,
    Lambda,
    UpSampling2D,
)
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.merge import concatenate
from keras.models import Model
import hashlib
import cryolo.utils as utils

dir_script = os.path.dirname(__file__)
init_weights = "https://ndownloader.figshare.com/files/16406843"  # ftp://ftp.gwdg.de/pub/misc/sphire/crYOLO-INIT/full_yolo_backend.h5'
init_weights_md5 = "647974a82106d7a0e5663a29a78a4598"
FULL_YOLO_BACKEND_PATH = os.path.join(dir_script, "full_yolo_backend.h5")


def download_model():
    import shutil
    import urllib.request as request
    from contextlib import closing

    if not os.path.exists(FULL_YOLO_BACKEND_PATH):
        try:
            with closing(request.urlopen(init_weights)) as r:

                with open(FULL_YOLO_BACKEND_PATH, "wb") as f:
                    shutil.copyfileobj(r, f)
                print("Wrote model for initilization to:", FULL_YOLO_BACKEND_PATH)
        except:
            print("############################################")
            print("Unable to download initialization weights from " + init_weights)
            print(
                "Try to download it manually from "
                + "https://figshare.com/articles/Initialization_weights_for_crYOLO/8965541"
            )
            print("and save it to " + dir_script)
            print("############################################")
            return None
    else:
        print("Initialization of model with " + FULL_YOLO_BACKEND_PATH)

    md5sum = hashlib.md5(open(FULL_YOLO_BACKEND_PATH, "rb").read()).hexdigest()
    if md5sum != init_weights_md5:
        print("Initial weights seems to be corrupted (md5sum comparision failed).")
        if os.path.exists(FULL_YOLO_BACKEND_PATH):
            print("Remove corrupted weights")
            os.remove(FULL_YOLO_BACKEND_PATH)
        return None
    return FULL_YOLO_BACKEND_PATH


def init_extractor(feature_extractor, backend_weights):
    if backend_weights == None:
        FULL_YOLO_BACKEND_PATH = download_model()
        if FULL_YOLO_BACKEND_PATH is not None:
            feature_extractor.load_weights(FULL_YOLO_BACKEND_PATH, by_name=True)
        else:
            print("Random initialisation of the network")
    else:
        print("Use custom backend path: ", backend_weights)
        feature_extractor.load_weights(backend_weights, by_name=True)


class BaseFeatureExtractor(object):
    """docstring for ClassName"""

    # to be defined in each subclass
    def __init__(self, input_size):
        raise NotImplementedError("error message")

    # to be defined in each subclass
    def normalize(self, image):
        raise NotImplementedError("error message")

    def get_output_shape(self):
        return self.feature_extractor.get_output_shape_at(-1)[1:3]

    def extract(self, input_image):
        return self.feature_extractor(input_image)


class CrYoloFeature(BaseFeatureExtractor):
    """docstring for ClassName"""

    def __init__(self, input_size, input_depth, backend_weights=None):

        input_image = Input(shape=(input_size[1], input_size[0], input_depth))

        # name of first layer
        name_first_layer = "conv_1"
        if input_depth == 1:
            name_first_layer = "conv_1_depth1"

        # the function to implement the orgnization layer (thanks to github.com/allanzelener/YAD2K)
        def space_to_depth_x2(x):
            import tensorflow as tf

            return tf.space_to_depth(x, block_size=2)

        # Layer 1
        x = Conv2D(
            32,
            (3, 3),
            strides=(1, 1),
            padding="same",
            name=name_first_layer,
            use_bias=False,
        )(input_image)
        x = BatchNormalization(name="norm_1")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 2
        x = Conv2D(
            64, (3, 3), strides=(1, 1), padding="same", name="conv_2", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_2")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 3
        x = Conv2D(
            128, (3, 3), strides=(1, 1), padding="same", name="conv_3", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_3")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 4
        x = Conv2D(
            64, (1, 1), strides=(1, 1), padding="same", name="conv_4", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_4")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 5
        x = Conv2D(
            128, (3, 3), strides=(1, 1), padding="same", name="conv_5", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_5")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 6
        x = Conv2D(
            256, (3, 3), strides=(1, 1), padding="same", name="conv_6", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_6")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 7
        x = Conv2D(
            128, (1, 1), strides=(1, 1), padding="same", name="conv_7", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_7")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 8
        x = Conv2D(
            256, (3, 3), strides=(1, 1), padding="same", name="conv_8", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_8")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 9
        x = Conv2D(
            512, (3, 3), strides=(1, 1), padding="same", name="conv_9", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_9")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 10
        x = Conv2D(
            256, (1, 1), strides=(1, 1), padding="same", name="conv_10", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_10")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 11
        x = Conv2D(
            512, (3, 3), strides=(1, 1), padding="same", name="conv_11", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_11")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 12
        x = Conv2D(
            256, (1, 1), strides=(1, 1), padding="same", name="conv_12", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_12")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 13
        x = Conv2D(
            512, (3, 3), strides=(1, 1), padding="same", name="conv_13", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_13")(x)
        x = LeakyReLU(alpha=0.1)(x)

        #
        # UP TO HERE - EVERYTHING IS THE SAME AS IN FULL YOLO
        #

        # Layer 14
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_14", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_14")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 15
        x = Conv2D(
            512, (1, 1), strides=(1, 1), padding="same", name="conv_15", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_15")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 16
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_16", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_16")(x)
        x = LeakyReLU(alpha=0.1)(x)

        self.feature_extractor = Model(input_image, x)
        init_extractor(self.feature_extractor, backend_weights)

    def normalize(self, image, margin_size=0):

        return utils.normalize(image, margin_size)


class PhosaurusNetFeature(BaseFeatureExtractor):
    """docstring for ClassName"""

    def __init__(self, input_size, input_depth, backend_weights=None):

        input_image = Input(shape=(input_size[1], input_size[0],input_depth))

        # name of first layer
        name_first_layer = "conv_1"
        if input_depth == 1:
            name_first_layer = "conv_1_depth1"

        # Layer 1
        x = Conv2D(
            32,
            (3, 3),
            strides=(1, 1),
            padding="same",
            name=name_first_layer,
            use_bias=False,
        )(input_image)
        x = BatchNormalization(name="norm_1")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 2
        x = Conv2D(
            64, (3, 3), strides=(1, 1), padding="same", name="conv_2", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_2")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 3
        x = Conv2D(
            128, (3, 3), strides=(1, 1), padding="same", name="conv_3", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_3")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 4
        x = Conv2D(
            64, (1, 1), strides=(1, 1), padding="same", name="conv_4", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_4")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 5
        x = Conv2D(
            128, (3, 3), strides=(1, 1), padding="same", name="conv_5", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_5")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 6
        x = Conv2D(
            256, (3, 3), strides=(1, 1), padding="same", name="conv_6", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_6")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 7
        x = Conv2D(
            128, (1, 1), strides=(1, 1), padding="same", name="conv_7", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_7")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 8
        x = Conv2D(
            256, (3, 3), strides=(1, 1), padding="same", name="conv_8", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_8")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 9
        x = Conv2D(
            512, (3, 3), strides=(1, 1), padding="same", name="conv_9", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_9")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 10
        x = Conv2D(
            256, (1, 1), strides=(1, 1), padding="same", name="conv_10", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_10")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 11
        x = Conv2D(
            512, (3, 3), strides=(1, 1), padding="same", name="conv_11", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_11")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 12
        x = Conv2D(
            256, (1, 1), strides=(1, 1), padding="same", name="conv_12", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_12")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 13
        x = Conv2D(
            512, (3, 3), strides=(1, 1), padding="same", name="conv_13", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_13")(x)
        x = LeakyReLU(alpha=0.1)(x)

        skip_connection = x

        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 14
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_14", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_14")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 15
        x = Conv2D(
            512, (1, 1), strides=(1, 1), padding="same", name="conv_15", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_15")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 16
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_16", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_16")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 17
        x = Conv2D(
            512, (1, 1), strides=(1, 1), padding="same", name="conv_17", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_17")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 18
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_18", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_18")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 19
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_19", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_19")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 20
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_20", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_20")(x)
        x = LeakyReLU(alpha=0.1)(x)

        x = UpSampling2D(size=(2, 2))(x)

        skip_connection = Conv2D(
            256, (1, 1), strides=(1, 1), padding="same", name="conv_21_", use_bias=False
        )(skip_connection)
        skip_connection = BatchNormalization(name="norm_21_")(skip_connection)
        skip_connection = LeakyReLU(alpha=0.1)(skip_connection)
        x = concatenate([skip_connection, x])

        # Layer 21
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_22", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_22")(x)
        x = LeakyReLU(alpha=0.1)(x)

        self.feature_extractor = Model(input_image, x)
        init_extractor(self.feature_extractor, backend_weights)

    def normalize(self, image, margin_size=0):

        return utils.normalize(image, margin_size)


class FullYoloFeature(BaseFeatureExtractor):
    """docstring for ClassName"""

    def __init__(self, input_size, input_depth, backend_weights=None):
        input_image = Input(shape=(input_size[1], input_size[0], input_depth))

        # name of first layer
        name_first_layer = "conv_1"
        if input_depth == 1:
            name_first_layer = "conv_1_depth1"

        # the function to implement the orgnization layer (thanks to github.com/allanzelener/YAD2K)
        def space_to_depth_x2(x):
            import tensorflow as tf

            return tf.space_to_depth(x, block_size=2)

        # Layer 1
        x = Conv2D(
            32,
            (3, 3),
            strides=(1, 1),
            padding="same",
            name=name_first_layer,
            use_bias=False,
        )(input_image)
        x = BatchNormalization(name="norm_1")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 2
        x = Conv2D(
            64, (3, 3), strides=(1, 1), padding="same", name="conv_2", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_2")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 3
        x = Conv2D(
            128, (3, 3), strides=(1, 1), padding="same", name="conv_3", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_3")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 4
        x = Conv2D(
            64, (1, 1), strides=(1, 1), padding="same", name="conv_4", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_4")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 5
        x = Conv2D(
            128, (3, 3), strides=(1, 1), padding="same", name="conv_5", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_5")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 6
        x = Conv2D(
            256, (3, 3), strides=(1, 1), padding="same", name="conv_6", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_6")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 7
        x = Conv2D(
            128, (1, 1), strides=(1, 1), padding="same", name="conv_7", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_7")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 8
        x = Conv2D(
            256, (3, 3), strides=(1, 1), padding="same", name="conv_8", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_8")(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 9
        x = Conv2D(
            512, (3, 3), strides=(1, 1), padding="same", name="conv_9", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_9")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 10
        x = Conv2D(
            256, (1, 1), strides=(1, 1), padding="same", name="conv_10", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_10")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 11
        x = Conv2D(
            512, (3, 3), strides=(1, 1), padding="same", name="conv_11", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_11")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 12
        x = Conv2D(
            256, (1, 1), strides=(1, 1), padding="same", name="conv_12", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_12")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 13
        x = Conv2D(
            512, (3, 3), strides=(1, 1), padding="same", name="conv_13", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_13")(x)
        x = LeakyReLU(alpha=0.1)(x)

        skip_connection = x

        x = MaxPooling2D(pool_size=(2, 2))(x)

        # Layer 14
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_14", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_14")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 15
        x = Conv2D(
            512, (1, 1), strides=(1, 1), padding="same", name="conv_15", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_15")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 16
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_16", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_16")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 17
        x = Conv2D(
            512, (1, 1), strides=(1, 1), padding="same", name="conv_17", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_17")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 18
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_18", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_18")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 19
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_19", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_19")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 20
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_20", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_20")(x)
        x = LeakyReLU(alpha=0.1)(x)

        # Layer 21
        skip_connection = Conv2D(
            64, (1, 1), strides=(1, 1), padding="same", name="conv_21", use_bias=False
        )(skip_connection)
        skip_connection = BatchNormalization(name="norm_21")(skip_connection)
        skip_connection = LeakyReLU(alpha=0.1)(skip_connection)
        skip_connection = Lambda(space_to_depth_x2)(skip_connection)

        x = concatenate([skip_connection, x])

        # Layer 22
        x = Conv2D(
            1024, (3, 3), strides=(1, 1), padding="same", name="conv_22", use_bias=False
        )(x)
        x = BatchNormalization(name="norm_22")(x)
        x = LeakyReLU(alpha=0.1)(x)

        self.feature_extractor = Model(input_image, x)
        init_extractor(self.feature_extractor, backend_weights)

    def normalize(self, image, margin_size=0):

        return utils.normalize(image, margin_size)
