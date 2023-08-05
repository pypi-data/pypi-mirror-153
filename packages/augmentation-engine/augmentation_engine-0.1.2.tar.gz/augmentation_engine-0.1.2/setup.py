import os
import setuptools
import CONSTANTS
from setuptools import find_packages
import glob

readme = "README.md"
requirement_path = CONSTANTS.Requirements_path
readme_path = os.path.join(os.path.dirname(__file__), readme)
with open(readme, "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open(requirement_path) as f:
    install_requires = f.read().splitlines()

pkgs = find_packages(exclude=['tests.*', 'tests'])

setuptools.setup(
    name="augmentation_engine",
    version="0.1.2",
    author="Shreejaa Talla",
    author_email="shreejaa.talla@gmail.com",
    description="Solar Filaments data augmentation demo package",
    url="https://bitbucket.org/gsudmlab/augmentation_engine/src/master/",
    project_urls={
        "Source": "https://bitbucket.org/gsudmlab/augmentation_engine/src/master/",
    },
    packages = pkgs,
    package_dir={"filament_augmentation": "filament_augmentation"},
    package_data={
        '.': ['requirements.txt']},
    install_requires=install_requires,
    py_modules=['CONSTANTS'],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)

