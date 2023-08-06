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

from keras.callbacks import ModelCheckpoint


class ExtendedModelCheckpoint(ModelCheckpoint):


    def __init__(self, *args, **kwargs):
        super(ExtendedModelCheckpoint,self).__init__(*args,**kwargs)
        self.fine_tune = None
        self.num_free_layers = None
        self.anchors = None
        self.version = None
        self.filament_model = False

    def set_fine_tune(self, fine_tune, num_free_layers):
        self.fine_tune = fine_tune
        self.num_free_layers = num_free_layers

    def set_anchors(self, anchors):
        self.anchors = anchors

    def set_filamet_model(self, is_filament_model):
        self.filament_model = is_filament_model

    def reset_best(self, best):
        self.best = best

    def set_version(self, version):
        self.version = version

    def on_epoch_end(self, epoch, logs=None):
        update = False
        current = logs.get(self.monitor)
        if current is not None:
            if self.monitor_op(current, self.best):
                update = True
        super(ExtendedModelCheckpoint, self).on_epoch_end(epoch, logs)

        if update:
            #############################################
            # Save meta data about the model
            #############################################
            import h5py

            with h5py.File(self.filepath, mode="r+") as f:
                f["anchors"] = self.anchors
                f["filament_model"] = [int(self.filament_model)]
                if self.fine_tune:
                    f["num_free_layers"] = [self.num_free_layers]
                if self.version is not None:
                    f["cryolo_version"] = [str(self.version).encode('utf8')]
