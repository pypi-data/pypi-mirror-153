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


class MultiGPUModelCheckpoint(ModelCheckpoint):

    def __init__(self, *args, **kwargs):
        super(MultiGPUModelCheckpoint,self).__init__(*args,**kwargs)
        self.template_model = None
        self.fine_tune = None
        self.anchors = None
        self.num_free_layers = None
        self.version = None
        self.filament_model = False

    def set_template_model(self, template_model):
        self.template_model = template_model

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
        current = logs.get(self.monitor)
        if current is not None:
            if self.monitor_op(current, self.best):
                if self.verbose > 0:
                    print(
                        "\nEpoch %05d: %s improved from %0.5f to %0.5f,"
                        " saving model to %s"
                        % (epoch + 1, self.monitor, self.best, current, self.filepath)
                    )
                self.best = current
                if self.save_weights_only:
                    self.template_model.save_weights(self.filepath, overwrite=True)
                else:
                    self.template_model.save(self.filepath, overwrite=True)

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

            else:
                if self.verbose > 0:
                    print(
                        "\nEpoch %05d: %s did not improve from %0.5f"
                        % (epoch + 1, self.monitor, self.best)
                    )

    # def set_model(self, model):
    #    model_copy = clone_model(self.template_model)
    #    model_copy.set_weights(self.template_model.get_weights())
    #    self.model = model_copy
    # if isinstance(model.layers[-2], Model):
    #    self.model = model.layers[-2]
    # else:
    #    self.model = model
