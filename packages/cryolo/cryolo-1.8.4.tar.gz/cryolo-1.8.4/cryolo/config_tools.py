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


def generate_config_file(
    config_out_path,
    architecture,
    input_size,
    anchors,
    max_box_per_image,
    num_patches,
    overlap_patches,
    filter,
    train_image_folder,
    train_annot_folder,
    train_times,
    pretrained_weights,
    batch_size,
    learning_rate,
    nb_epoch,
    object_scale,
    no_object_scale,
    coord_scale,
    class_scale,
    log_path,
    saved_weights_name,
    debug,
    valid_image_folder,
    valid_annot_folder,
    valid_times,
    normalization,
):

    model_dict = {
        "architecture": architecture,
        "input_size": input_size,
        "anchors": anchors,
        "max_box_per_image": max_box_per_image,
        "norm": normalization,
    }
    if num_patches > 1:
        model_dict["num_patches"] = num_patches
        model_dict["overlap_patches"] = overlap_patches

    if filter is not None:
        model_dict["filter"] = filter
    dict = {"model": model_dict}
    # "train": train_dict, "valid": valid_dict
    if train_image_folder or train_annot_folder:
        train_dict = {
            "train_image_folder": train_image_folder,
            "train_annot_folder": train_annot_folder,
            "train_times": train_times,
            "pretrained_weights": pretrained_weights,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "nb_epoch": nb_epoch,
            "object_scale": object_scale,
            "no_object_scale": no_object_scale,
            "coord_scale": coord_scale,
            "class_scale": class_scale,
            "saved_weights_name": saved_weights_name,
            "debug": debug,
        }
        dict["train"] = train_dict

        valid_dict = {
            "valid_image_folder": valid_image_folder,
            "valid_annot_folder": valid_annot_folder,
            "valid_times": valid_times,
        }
        dict["valid"] = valid_dict
    if log_path:
        other_dict = {
            "log_path": log_path,
        }
        dict["other"] = other_dict

    from json import dump

    with open(config_out_path, "w") as f:
        dump(dict, f, ensure_ascii=False, indent=4)
    print("\n Wrote config to", config_out_path)


def get_number_patches(config):
    """
    Returns the number of patches in config file.
    :param config: config dictionary
    :return: Number of patches
    """
    if "num_patches" in config["model"]:
        num_patches = config["model"]["num_patches"]
    else:
        num_patches = 1

    return num_patches


def adjust_size(size):
    if type(size) == list:
        return [int(32 * round(float(s) / 32)) for s in size]
    return int(32 * round(float(size) / 32))

def get_adjusted_input_size(config):
    if type(config["model"]["input_size"]) != list:
        new_input_size = adjust_size([config["model"]["input_size"]])[0]
    else:
        new_input_size = adjust_size(config["model"]["input_size"])

    if ( new_input_size != config["model"]["input_size"]
    ):
        print(
            "You input size",
            "(",
            config["model"]["input_size"],
            ")",
            "is not a multiple of 32. Round it to the next multiple of 32:",
            new_input_size,
        )
    return new_input_size


def get_gridcell_dimensions(config):
    """
    Returns the grid cell dimension in dependence of the use network.
    :param config: config dictionary
    :return: grid cell dimensions
    """
    if config["model"]["architecture"] == "YOLO":
        downsampling_factor = 32.0
    elif (
        config["model"]["architecture"] == "crYOLO"
        or config["model"]["architecture"] == "PhosaurusNet"
    ):
        downsampling_factor = 16.0
    else:
        raise Exception(
            "Architecture not supported! "
            "Only support for PhosaurusNet, YOLO and crYOLO at the moment!"
        )

    if type(config["model"]["input_size"]) is list and len(config["model"]["input_size"])==2:
        grid_w = config["model"]["input_size"][0] / downsampling_factor
        grid_h = config["model"]["input_size"][1] / downsampling_factor
    else:
        grid_w = config["model"]["input_size"] / downsampling_factor
        grid_h = grid_w


    return grid_w, grid_h


"""
def get_export_size(config):
    if "particle_diameter" in config["model"]:
        if isinstance(config["model"]["particle_diameter"], list):
            export_size = config["model"]["particle_diameter"][0]
        else:
            export_size = config["model"]["particle_diameter"]
    elif len(config["model"]["anchors"]) == 2:
        export_size = config["model"]["anchors"][0]
    else:
        export_size = None
"""


def get_box_size(config):
    """
    Read the box size from the config.

    :param config:
    :return: Box size
    """
    if "particle_diameter" in config["model"]:
        box_height = config["model"]["particle_diameter"]
        box_width = config["model"]["particle_diameter"]
    elif "anchors" in config["model"]:
        if len(config["model"]["anchors"]) == 2:
            box_height, box_width = config["model"]["anchors"]
    else:
        box_height, box_width = 0, 0
    return box_width, box_height
