from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Shortcuts funcitions.'
LONG_DESCRIPTION = 'These are functions that facilitate certain actions. Which needs to cite some parts for it to work.'

# Setting up
setup(
    name="Shōtokatan",
    version=VERSION,
    author="Aleph (Lotexiu)",
    author_email="<alephcostamelo@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/lotexiu/Sh-tokatan',
    packages=find_packages(),
    install_requires=['keyboard', 'pyautogui', 'pydirectinput', 'Pillow', 'mido'],
    keywords=['python', 'sqlite', 'keyboard', 'pixel capture', 'Pillow', 'teminal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)