import os
import setuptools

setuptools.setup(
    name='generic_behave',
    version=os.environ.get("BUILD_VERSION", "0.0.0.dev-1"),
    package_dir = {'': 'test_utils'},
    packages=['behave.src.ns_behave',
              'behave.src.ns_behave.common',
              'behave.src.ns_behave.models',
              'behave.src.ns_behave.step_library.generic_behave_steps',
              'page_objects.src.ns_page_objects',
              'page_objects.src.ns_page_objects.selenium_functions',
              'page_objects.src.ns_page_objects.utils',
              'requests.src.ns_requests'
              ],
    install_requires=open("requirements.txt").readlines(),
)
