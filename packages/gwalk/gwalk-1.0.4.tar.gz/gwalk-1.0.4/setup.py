"""
GWALK: Gravitational Wave Approximate Likelihood Kernel estimates

Vera Del Favero
"""

from datetime import date
from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize

#----------------------------------------------------------------
# General
#----------------------------------------------------------------

__name__        = "gwalk"
__version__     = "1.0.4"
__date__        = date(2022, 6, 6)
__keywords__    = [
    "Gravitational Wave",
    "Likelihood",
    ]
__status__      = "Alpha"

#----------------------------------------------------------------
# URLs
#----------------------------------------------------------------
__url__         = "https://gitlab.com/xevra/gwalk"
__bugtrack_url__= "https://gitlab.com/xevra/gwalk/issues"


#----------------------------------------------------------------
# People
#----------------------------------------------------------------

__author__      = "Vera Del Favero"
__author_email__= "msd8070@rit.edu"

__maintainer__  = "Vera Del Favero"
__maintainer_email__= "msd8070@rit.edu"

__credits__     = ("Vera Del Favero")

#----------------------------------------------------------------
# Legal
#----------------------------------------------------------------
__copyright__   = "Copyright (c) 2019 {author} <{email}>".format(
    author = __author__,
    email = __author_email__
    )

__license__ = "MIT Lisence"
__licence_full__ = '''
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

#----------------------------------------------------------------
# Package
#----------------------------------------------------------------

ext_modules = [
    Extension(
              "relative_entropy_cython",
              sources=["src/gwalk/utils/relative_entropy_cython.pyx"],
              libraries=["m"],
              include_dirs=["src/gwalk/utils/"],
             ),
    Extension(
              "maha_cython",
              sources=["src/gwalk/utils/maha_cython.pyx"],
              libraries=["m"],
              include_dirs=["src/gwalk/utils/"],
             ),
    Extension(
              "probability_distances_cython",
              sources=["src/gwalk/utils/probability_distances_cython.pyx"],
              libraries=["m"],
              include_dirs=["src/gwalk/utils/"],
             ),
              ]

DOCLINES = __doc__.split("\n")

CLASSIFIERS = """
Development Status :: 3 - Alpha
Programming Language :: Python :: 3
Operating System :: OS Independent
Intended Audience :: Science/Research
Topic :: Scientific/Engineering :: Astronomy
Topic :: Scientific/Engineering :: Physics
Topic :: Scientific/Engineering :: Information Analysis
""".strip()

#		"scikit-sparse>=0.4.4",
REQUIREMENTS = {
    "install" : [
        "numpy>=1.16",
        "matplotlib>=2.2.4",
        "scipy>=1.5.0",
        "h5py>=2.10.0",
        "cython>=3.0.0a10",
        "astropy>=4.0",
        "gaussian-process-api>=0.3.3",
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
	]
}

from setuptools import find_packages, setup

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

    classifiers=[f for f in CLASSIFIERS.split('\n') if f],

    package_dir ={"": "src"},
    packages=find_packages("src"),

    install_requires=REQUIREMENTS["install"],
    setup_requires=REQUIREMENTS["setup"],
    tests_require=REQUIREMENTS["tests"],
    entry_points=ENTRYPOINTS,
    ext_modules=cythonize(ext_modules),
    python_requires=">3.6",
)

setup(**metadata)

