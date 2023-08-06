# See LICENSE for details

"""The setup script."""
import os
from setuptools import setup, find_packages

# Base directory of package
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()
def read_requires():
    with open(os.path.join(here, "aapg/requirements.txt"),"r") as reqfile:
        return reqfile.read().splitlines()

#Long Description
#with open("README.rst", "r") as fh:
#    readme = fh.read()

setup_requirements = [ ]

test_requirements = [ ]

setup(
    name='aapg',
    version='2.3.0',
    description="RISC-V AAPG",
    long_description=' AAPG \n\n',
    classifiers=[
          "Programming Language :: Python :: 3.6",
          "License :: OSI Approved :: BSD License",
          "Development Status :: 4 - Beta"
    ],
    url='https://gitlab.com/shaktiproject/tools/aapg',
    author="",
    author_email='shakti.iitm@gmail.com',
    license="MIT license",
    packages=find_packages(),
    package_dir={'aapg': 'aapg'},
    install_requires=read_requires(),
    python_requires='>=3.6.0',
    entry_points={
        'console_scripts': ['aapg=aapg.main:cli'],
    },
    include_package_data=True,
    keywords='aapg',
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False,
)
