import setuptools
import sys
# Workaround for dynamic version reading..
sys.path[0:0] = ['tendrils']
from version import version as __version__  # noqa: E402
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='tendrils',
    version=__version__,
    author="Emir Karamehmetoglu, Rasmus Handberg",
    author_email="emirkmo@github.com",
    description="Tendrils: API for accessing flows pipeline and data products.",
    long_description=long_description,
    packages=setuptools.find_packages(),
    license="LICENSE.rst",
    url="https://github.com/SNFLOWS/tendrils",
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                 "Operating System :: OS Independent",
                 "Topic :: Scientific/Engineering :: Astronomy"],
    python_requires='>=3.10',
    install_requires=['numpy',
                      'astropy',
                      'requests',
                      'tqdm',
                      ],
    package_data={"tendrils": ["utils/*.ini"]}  # include any .ini found in utils.
)
