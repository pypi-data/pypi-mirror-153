import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

exec(open('time_study_preprocessing_main/_version.py').read())

setuptools.setup(
    name='microt_preprocessing',
    version=__version__,
    description='A package that transforms raw sensor data collected from Time study app into intermediate CSV file '
                'for analysis of various purposes',
    url='https://bitbucket.org/mhealthresearchgroup/microt_preprocessing/src/master/',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jixin Li, Aditya Ponnada',
    author_email='li.jix@northeastern.edu',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7'
)