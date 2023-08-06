import glob
import pathlib
from setuptools import find_packages, setup
from inspec_ai import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# data files (non-python modules) to be included in the package
assets = glob.glob("inspec_ai/quality/visualisation/assets/**/*.*", recursive=True)
templates = glob.glob("inspec_ai/quality/visualisation/templates/**/*.*", recursive=True)
data_files = [("inspec_ai", assets + templates)]

setup(
    name="inspec-ai",
    version=__version__,
    license="Internal Use",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="Library containing all the prototypes that were developped by the Moov AI product team.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://moov.ai/en/",
    author="MoovAI Technologies Inc",
    author_email="info@moov.ai",
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    install_requires=[
        "colorama==0.4.4",
        "holidays==0.12",
        "jinja2==3.0.3",
        "kaggle==1.5.12",
        "matplotlib==3.5.1",
        "numpy==1.21.3",
        "pandas==1.3.4",
        "pandas-profiling==3.1.0",
        "pillow==9.1.0",
        "scikit-learn==1.0.2",
        "fuzzywuzzy==0.18.0",
    ],
    entry_points={},
    data_files=data_files,
)
