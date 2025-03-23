from setuptools import setup, find_packages

VERSION = "0.2.0"
DESCRIPTION = "Supplement nbgrader with unit-test-based partial grading."
LONG_DESCRIPTION = "A small utility library for unit testing student-submitted code. Intended for use with nbgrader, but not strictly necessary."

setup(
    name="nbgrader_utils",
    version=VERSION,
    author="Jason Balaci",
    author_email="balacij@mcmaster.ca",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["jupyter", "nbgrader"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Jupyter :: JupyterLab" "Topic :: Education :: Testing",
    ],
)
