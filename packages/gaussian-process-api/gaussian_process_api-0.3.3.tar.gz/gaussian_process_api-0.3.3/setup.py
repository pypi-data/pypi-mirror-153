"""\
gaussian-process-api for efficient regression.

Long description goes here...
"""

from datetime import date
from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize


#-------------------------------------------------------------------------------
#   GENERAL
#-------------------------------------------------------------------------------
__name__        = "gaussian_process_api"
__version__     = "0.3.3"
__date__        = date(2022, 4, 11)
__keywords__    = [
    "astronomy",
    "information analysis",
    "machine learning",
    "physics",
]
__status__      = "Alpha"


#-------------------------------------------------------------------------------
#   URLS
#-------------------------------------------------------------------------------
__url__         = "https://gitlab.com/xevra/gaussian-process-api"
__bugtrack_url__= "https://gitlab.com/xevra/gaussian-process-api/issues"


#-------------------------------------------------------------------------------
#   PEOPLE
#-------------------------------------------------------------------------------
__author__      = "Vera Delfavero, Daniel Wysocki, Richard O'Shaughnessy"
__author_email__= "xevra86@gmail.com"

__maintainer__      = "Vera Delfavero"
__maintainer_email__= "xevra86@gmail.com"

__credits__     = ("Vera Delfavero", "Daniel Wysocki", "Richard O'Shaughnessy",)


#-------------------------------------------------------------------------------
#   LEGAL
#-------------------------------------------------------------------------------
__copyright__   = 'Copyright (c) 2022 {author} <{email}>'.format(
    author=__author__,
    email=__author_email__
)

__license__     = 'MIT License'
__license_full__= '''
MIT License

{copyright}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''.format(copyright=__copyright__).strip()


#-------------------------------------------------------------------------------
#   PACKAGE
#-------------------------------------------------------------------------------

ext_modules = cythonize(
              [
               Extension("compact_kernel_cython",
                         sources=["src/gp_api/kernels/compact_kernel_cython.pyx"],
                         libraries=["m"],
                         include_dirs=["src/gp_api/kernels/"],
                        ),
               Extension("matern_kernel_cython",
                         sources=["src/gp_api/kernels/matern_kernel_cython.pyx"],
                         libraries=["m"],
                         include_dirs=["src/gp_api/kernels/"],
                        ),
              ])

#PACKAGE_DATA = {
#    "": [],
#}

DOCLINES = __doc__.split("\n")

CLASSIFIERS = [
"Development Status :: 3 - Alpha",
"Programming Language :: Python :: 3",
"Operating System :: OS Independent",
"Intended Audience :: Science/Research",
"Topic :: Scientific/Engineering :: Astronomy",
"Topic :: Scientific/Engineering :: Physics",
"Topic :: Scientific/Engineering :: Information Analysis",
]

REQUIREMENTS = {
    "install" : [
        "h5py>=2.7.0",
        "numpy>=1.16.0",
        "matplotlib>=2.0.0",
        "scipy>=1.2.0",
        "six>=1.10.0",
        "scikit-sparse>= 0.4.0",
        "cython>=3.0.0a10",
        "fast_histogram>=0.10"
    ],
    "setup" : [
        "pytest-runner",
    ],
    "tests" : [
        "pytest",
    ]
}

ENTRYPOINTS = {
    "console_scripts" : [
        # Example:
        # script_name = module.2.import:function_to_call
    ]
}


metadata = dict(
    name        =__name__,
    version     =__version__,
    description =DOCLINES[0],
    long_description='\n'.join(DOCLINES[2:]),
    keywords    =__keywords__,

    author      =__author__,
    author_email=__author_email__,

    maintainer  =__maintainer__,
    maintainer_email=__maintainer_email__,

    url         =__url__,
#    download_url=__download_url__,

    license     =__license__,

    classifiers=CLASSIFIERS,

    package_dir ={"": "src"},
    packages=find_packages("src"),

    install_requires=REQUIREMENTS["install"],
    setup_requires=REQUIREMENTS["setup"],
    tests_require=REQUIREMENTS["tests"],

    entry_points=ENTRYPOINTS,
    ext_modules=ext_modules,
    python_requires=">=3.6",
)

setup(**metadata)
