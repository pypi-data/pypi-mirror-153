import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE/"PYPI_README.md").read_text()

setup(
    name="kawaplatformlibrary",
    version="1.0",
    description="Library for Data Ingestion",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/KawaSpaceOrg/kawaplatformlibrary",
    license_files = ("LICENSE.md"),
    author="Gotam",
    author_email="gotamdahiya@gmail.com",
    packages=find_packages(exclude=("bin", "lib", "examples", "test" )),
    include_package_data=True,
    install_requires=["joblib==1.1.0", "numpy==1.22.0", "pandas==1.0.5", "python_dateutil==2.8.2", "rasterio==1.2.10", "requests==2.22.0", "scikit_learn==1.0.2", "Shapely==1.7.1"],
    python_requires='>=3.8'
    )