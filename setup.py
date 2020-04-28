import os
import setuptools

setuptools.setup(
    name='generic_behave',
    version=os.environ.get("BUILD_VERSION", "0.0.0.dev-1"),
    packages=['test_utils.behave.src.ns_behave', 'test_utils.requests.src.ns_requests', 'test_utils.page_objects.src.ns_page_objects'],
    install_requires=open("requirements.txt").readlines(),
)
