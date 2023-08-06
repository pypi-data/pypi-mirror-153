"""
This modules handels provides a callback that allows to train and warmup crYOLO in a single run
without restarting.
"""
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

import keras.backend as K
from keras.callbacks import Callback
import numpy as np

# pylint: disable=C0330


class WarmupCallback(Callback):
    """
    Callback to allow
    """

    def __init__(
        self,
        warmup_bs,
        num_warmup_epochs,
        len_train_img,
        len_valid_img,
        batch_size,
        num_patches,
        train_times,
        valid_times,
        early_stop_callback,
        modelcheckpoint,
        reduceonnplateau,
    ):
        """
        Adapts warmup_bs according to the epoch. This value is used in the loss function need to
        be changed for warmup-epochs and normal-epochs respectivly. Beside
        :param warmup_bs: A keras variable that is used in the loss function
        :param num_warmup_epochs:
        :param len_train_img: Number of training images
        :param len_valid_img:
        :param batch_size:
        :param num_patches:
        :param train_times:
        :param valid_times:
        :param early_stop_callback: Keras callback that has to be reset when changing
        from warmup-training to normal-training
        :param modelcheckpoint:  Keras callback that has to be reset when changing
        from warmup-training to normal-training
        :param reduceonnplateau: Keras callback that has to be reset when changing
        from warmup-training to normal-training
        """
        super().__init__()
        self.warmup_bs = warmup_bs
        self.num_warmup_epochs = num_warmup_epochs
        self.len_train_img = len_train_img
        self.len_valid_img = len_valid_img
        self.num_patches = num_patches
        self.batch_size = batch_size
        self.train_times = train_times
        self.valid_times = valid_times
        self.early_stop_callback = early_stop_callback
        self.modelcheckpoint = modelcheckpoint
        self.reduceonnplateau = reduceonnplateau

    def on_epoch_end(self, epoch, logs={}):
        """
        Add the end of the epoch we might have to change the the warmup_bs variable
        :param epoch: Current epoch
        :param logs:
        :return: None
        """
        if epoch == self.num_warmup_epochs - 1:
            if self.num_warmup_epochs > 0:
                print("###############")
                print("Warm up done.")
                print("###############")
            warmup_bs_help = 0.0
            self.early_stop_callback.on_train_begin()
            self.reduceonnplateau.on_train_begin()
            self.modelcheckpoint.reset_best(np.Inf)
            K.set_value(self.warmup_bs, warmup_bs_help)
        elif epoch < self.num_warmup_epochs:
            warmup_bs_help = self.num_warmup_epochs * (
                self.train_times
                * (
                    self.len_train_img
                    * self.num_patches
                    * self.num_patches
                    / self.batch_size
                    + 1
                )
                + self.valid_times
                * (
                    self.len_valid_img
                    * self.num_patches
                    * self.num_patches
                    / self.batch_size
                    + 1
                )
            )
            K.set_value(self.warmup_bs, warmup_bs_help)
