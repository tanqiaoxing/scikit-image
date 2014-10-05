#! /usr/bin/env python

descr = """Image Processing SciKit

Image processing algorithms for SciPy, including IO, morphology, filtering,
warping, color manipulation, object detection, etc.

Please refer to the online documentation at
http://scikit-image.org/
"""

DISTNAME            = 'scikit-image'
DESCRIPTION         = 'Image processing routines for SciPy'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Stefan van der Walt'
MAINTAINER_EMAIL    = 'stefan@sun.ac.za'
URL                 = 'http://scikit-image.org'
LICENSE             = 'Modified BSD'
DOWNLOAD_URL        = 'http://github.com/scikit-image/scikit-image'
VERSION             = '0.11dev'
PYTHON_VERSION      = (2, 6)

import re
import os
import sys

import setuptools
from distutils.command.build_py import build_py


# These are manually checked.
# These packages are sometimes installed outside of the setuptools scope
DEPENDENCIES = {}
with open('requirements.txt', 'rb') as fid:
    data = fid.read().decode('utf-8', 'replace')
for line in data.splitlines():
    pkg, _, version_info = line.partition('>=')
    # Only require Cython if we have a developer checkout
    if pkg.lower() == 'cython' and not VERSION.endswith('dev'):
        continue
    version = []
    for part in re.split('\D+', version_info):
            try:
                version.append(int(part))
            except ValueError:
                pass
    DEPENDENCIES[pkg.lower()] = tuple(version)


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    config.set_options(
            ignore_setup_xxx_py=True,
            assume_default_configuration=True,
            delegate_options_to_subpackages=True,
            quiet=True)

    config.add_subpackage('skimage')
    config.add_data_dir('skimage/data')

    return config


def write_version_py(filename='skimage/version.py'):
    template = """# THIS FILE IS GENERATED FROM THE SKIMAGE SETUP.PY
version='%s'
"""

    vfile = open(os.path.join(os.path.dirname(__file__),
                              filename), 'w')

    try:
        vfile.write(template % VERSION)
    finally:
        vfile.close()


def get_package_version(package):
    for version_attr in ('version', 'VERSION', '__version__'):
        version_info = getattr(package, version_attr, None)
        try:
            parts = re.split('\D+', version_info)
        except TypeError:
            continue
        for part in parts:
            try:
                version.append(int(part))
            except ValueError:
                pass

    return tuple(version)


def check_requirements():
    if sys.version_info < PYTHON_VERSION:
        raise SystemExit('You need Python version %d.%d or later.' \
                         % PYTHON_VERSION)

    for package_name, min_version in DEPENDENCIES.items():
        if package_name == 'cython':
            package_name = 'Cython'
        dep_error = False
        if package_name.lower() == 'pillow':
            package_name = 'PIL.Image'
        try:
            package = __import__(package_name,
                fromlist=[package_name.split('.')[-1]])
        except ImportError:
            dep_error = True
        else:
            package_version = get_package_version(package)
            if min_version > package_version:
                dep_error = True

        if dep_error:
            raise ImportError('You need `%s` version %s or later.' \
                              % (package_name, '.'.join(str(i) for i in min_version)))


if __name__ == "__main__":

    check_requirements()

    write_version_py()

    from numpy.distutils.core import setup
    setup(
        name=DISTNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        url=URL,
        license=LICENSE,
        download_url=DOWNLOAD_URL,
        version=VERSION,

        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: C',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
        ],

        configuration=configuration,
        install_requires=[
            "six>=%s" % '.'.join(str(d) for d in DEPENDENCIES['six'])
        ],
        packages=setuptools.find_packages(exclude=['doc']),
        include_package_data=True,
        zip_safe=False, # the package can run out of an .egg file

        entry_points={
            'console_scripts': ['skivi = skimage.scripts.skivi:main'],
        },

        cmdclass={'build_py': build_py},
    )
