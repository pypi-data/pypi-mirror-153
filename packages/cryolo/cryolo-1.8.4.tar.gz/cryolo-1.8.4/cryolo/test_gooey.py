from gooey import Gooey
import argparse
import multiprocessing
import time
import numpy as np
from scipy.spatial import cKDTree


class testclass:
    def __init__(self):
        self.ones = np.ones((4096, 4096))
        pass

    def test(self, i):

        print("Sleep", i)
        time.sleep(10)
        print("Done", i)


my_global_array = []


def _main_():
    # multiprocessing.set_start_method("spawn")
    import os
    import sys

    if len(sys.argv) >= 2:
        if not "--ignore-gooey" in sys.argv:
            sys.argv.append("--ignore-gooey")

    app = Gooey(
        main,
        program_name="crYOLO ",
        image_dir=os.path.join(os.path.abspath(os.path.dirname(__file__)), "../icons"),
        progress_regex=r"^.* \( Progress:\s+(-?\d+) % \)$",
        disable_progress_bar_animation=True,
        tabbed_groups=True,
        default_size=(1024, 630),
    )()
    print(app)


def main():
    parent = argparse.ArgumentParser(description="My program")
    parent.add_argument("-p", "--para", help="A parameter")

    args = parent.parse_args()
    global my_global_array
    for k in range(10):
        my_global_array.append(testclass())
    poolargs = []

    for i in range(10):
        poolargs.append((testclass(), i))

    pool = multiprocessing.Pool()
    pool.map(wrapper, poolargs)


def wrapper(arg):
    obj, i = arg
    print(my_global_array)
    obj.test(i)


if __name__ == "__main__":
    _main_()
