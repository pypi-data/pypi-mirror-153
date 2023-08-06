from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.9'
DESCRIPTION = 'SQL Server,CSV & JSON Connection Objects and Tools'

# Setting up
setup(
    name="martenczuk",
    version=VERSION,
    author="Kamil Martenczuk",
    author_email="<kamil.martenczuk@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pypyodbc', 'tqdm'],
    keywords=['python', 'sql', 'csv', 'json'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
