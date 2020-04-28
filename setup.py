import os
import setuptools

setuptools.setup(
    name='generic_behave',
    version=os.environ.get("BUILD_VERSION", "0.0.0.dev-1"),
    py_modules=(['ns_behave', 'ns_page_objects', 'ns_requests']),
    install_requires=open("requirements.txt").readlines(),
)
