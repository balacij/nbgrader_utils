from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="nbgrader_utils", 
        version=VERSION,
        author="Jason Balaci",
        author_email="balacij@mcmaster.ca",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['jupyter', 'nbgrader'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Framework :: Jupyter :: JupyterLab"
            "Topic :: Education :: Testing",
        ]
)
