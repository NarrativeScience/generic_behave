import os

import setuptools

setuptools.setup(
    name="generic_behave",
    version=os.environ.get("BUILD_VERSION", "0.0.0.dev-1"),
    packages=setuptools.find_packages(),
)