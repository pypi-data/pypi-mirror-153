from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Setup for GUI Mail Client'
LONG_DESCRIPTION = 'A "module" that basically installs all the required module for GUI Mail Client'

# Setting up
setup(
    name="gui-mail-client-setup",
    version=VERSION,
    author="Markandpreston",
    author_email="<altmarc79@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pyqt5', 'winotify'],
    keywords=['python', 'email', 'setup'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)