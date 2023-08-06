from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Random augmentation for text, Thanks to NLP week Professors and instructors at National University of Ireland, Galway'
LONG_DESCRIPTION = 'Inspired by state-of-the-art data augmentation technique, RandAug, we propose Text random data augmentation, that use randAug approach for text data, \n Description of function is parameteres: \n training original: is input file in txt format, each line have a label separated from sentence by tab \n  output file: output file path \n        alpha_sr: parameter for controlling replacement \n       alpha_ri: parameter for controlling random insertion  \n alpha_rs: parameter for controlling random swaping \n  alpha_rd: parameter for controlling random deletion \n num_aug: is number of augmentation, by default 9'

# Setting up
setup(
    name="TextRandAug",
    version=VERSION,
    author="Jovan Jeromela,Liam De La Cour , Aaron Flannagan, Amandeep Singh and Teerath Kumar",
    author_email="i141637@nu.edu.pk",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['nltk','textaugment'],
    keywords=['python', 'text data augmentation', 'random augmentation', 'randAug'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)