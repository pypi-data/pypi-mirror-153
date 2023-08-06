from setuptools import setup
import os
import re
import codecs
import sys
import setuptools
from distutils.command.sdist import sdist
from setuptools.command.install import install
# Create new package with python setup.py sdist



here = os.path.abspath(os.path.dirname(__file__))


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def binaries_directory(self):
        import os, sys, site
        """Return the installation directory, or None"""
        if '--user' in sys.argv:
            paths = (site.getusersitepackages(),)
        else:
            py_version = '%s.%s' % (sys.version_info[0], sys.version_info[1])
            paths = (s % (py_version) for s in (
                sys.prefix + '/lib/python%s/dist-packages/',
                sys.prefix + '/lib/python%s/site-packages/',
                sys.prefix + '/local/lib/python%s/dist-packages/',
                sys.prefix + '/local/lib/python%s/site-packages/',
                '/Library/Python/%s/site-packages/',
            ))

        for path in paths:
            if os.path.exists(path):
                return path
        print('no installation path found', file=sys.stderr)
        return None

    def run(self):
        dir_script = os.path.join(self.binaries_directory(),"cryolo")
        init_weights = (
            "https://ndownloader.figshare.com/files/16406843"
        )  # ftp://ftp.gwdg.de/pub/misc/sphire/crYOLO-INIT/full_yolo_backend.h5'
        init_weights_md5 = "647974a82106d7a0e5663a29a78a4598"
        FULL_YOLO_BACKEND_PATH = os.path.join(dir_script, "full_yolo_backend.h5")
        import shutil
        import urllib.request as request
        import hashlib

        from contextlib import closing
        if not os.path.exists(dir_script):
            os.makedirs(dir_script)

        if not os.path.exists(FULL_YOLO_BACKEND_PATH):
            try:
                with closing(request.urlopen(init_weights)) as r:

                    with open(FULL_YOLO_BACKEND_PATH, "wb") as f:
                        shutil.copyfileobj(r, f)
                    print("Wrote model for initilization to:", FULL_YOLO_BACKEND_PATH)
            except Exception as e:
                print(e)
                print("############################################")
                print("Unable to download initialization weights from " + init_weights)
                print(
                    "Try to download it manually from "
                    + "https://figshare.com/articles/Initialization_weights_for_crYOLO/8965541"
                )
                print("and save it to " + dir_script)
                print("############################################")
        md5sum = hashlib.md5(open(FULL_YOLO_BACKEND_PATH, "rb").read()).hexdigest()
        if md5sum != init_weights_md5:
            print("Initial weights seems to be corrupted (md5sum comparision failed).")
            if os.path.exists(FULL_YOLO_BACKEND_PATH):
                print("Remove corrupted weights")
                os.remove(FULL_YOLO_BACKEND_PATH)
        install.run(self)


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    print("==========================================",sys.argv)
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cryolo',
    version=find_version("cryolo", "__init__.py"),
    python_requires='>=3.5.0, <3.9',
    packages=['cryolo','cryolo.augmentation','cryolo.evaluation','tests'],
    url='https://cryolo.readthedocs.io/en/stable/index.html',
    license='Other/Proprietary License (all rights reserved)',
    author='Thorsten Wagner',
    include_package_data=True,
    cmdclass={
        'install':PostInstallCommand
    },
    package_data={'cryolo': ['../icons/config_icon.png','../icons/program_icon.ico','../icons/program_icon.png']},
    setup_requires=["Cython"],
    extras_require={
        'gpu':  ['tensorflow-gpu == 1.15.4','janni[gpu] >= 0.3.0b5'],
        'cpu': ['tensorflow == 1.15.4', 'janni[cpu] >= 0.3.0b5'],
        'c11':  ['nvidia-tensorflow[horovod] < 1.16, >= 1.15.5+nv22.1','janni >= 0.3.0b5'],
    },
    install_requires=[
        "mrcfile >= 1.3.0",
        "Cython",
        "Keras == 2.3.1",
        "numpy >= 1.16.0, < 1.19.0",
        "h5py >= 2.5.0, < 3.0.0",
        "imageio >= 2.3.0",
        "Pillow >= 6.0.0",
        "tifffile==2020.9.3",
        "networkx",
        "scipy >= 1.3.0",
        "terminaltables",
        "lineenhancer == 1.0.9.dev2",
        "cryoloBM >= 1.4.0",
        "ansi2html",
        "GooeyDev >= 1.0.8b4",
        "wxPython >= 4.1.0",
        "scikit-learn==0.23.2",
        "pyStarDB==0.3.1",
        "trackpy",
        "pandas==1.1.4",
        "watchdog",
        "tqdm",
        "protobuf==3.20.0"

    ],
    author_email='thorsten.wagner@mpi-dortmund.mpg.de',
    description='Picking procedure for cryo em single particle analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'cryolo_train.py = cryolo.train:_main_',
            'cryolo_predict.py = cryolo.predict:_main_',
            'cryolo_evaluation.py = cryolo.eval:_main_',
            'cryolo_evaluation_tomo.py = cryolo.evaluation.tomoevaluation:_main_',
            'cryolo_gui.py = cryolo.cryolo_main:_main_']},
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'Environment :: X11 Applications',
                 'Intended Audience :: End Users/Desktop',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Scientific/Engineering :: Bio-Informatics',
                 'Programming Language :: Python :: 3',
                 'License :: Other/Proprietary License'],
)
