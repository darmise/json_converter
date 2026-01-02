from setuptools import setup, find_packages

setup(
    name="json_converter",           # nome del pacchetto
    version="0.1",
    packages=find_packages(where="src"),  # cerca pacchetti dentro src
    package_dir={"": "src"},         # mappa la root dei pacchetti a src
)
