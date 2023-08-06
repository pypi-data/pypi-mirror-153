import os
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.2'

DESCRIPTION = 'DRF temporary token authentication'

# Setting up
setup(
    name="drf-temptoken",
    version=VERSION,
    author="Kapustlo",
    description=DESCRIPTION,
    url='https://notabug.org/kapustlo/drf-temptoken',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=(
        'python', 
        'python3', 
        'django', 
        'drf', 
        'djangorestframework', 
        'django rest framework',
        'token',
        'temptoken',
        'temporary'
    ),
    classifiers=(
        "Framework :: Django",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Internet :: WWW/HTTP",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ),
    python_requires=">=3.8",
    install_requires=(
        'django',
        'djangorestframework'
    )
)
