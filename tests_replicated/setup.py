import os

import setuptools

setuptools.setup(
    name='ns_tests_replicated',
    version=os.environ.get("BUILD_VERSION", "0.0.0.dev-1"),
    package_dir={"": "src"},
    packages=setuptools.find_packages(include=['ns_behave', 'ns_page_objects', 'ns_requests']),
    provides=setuptools.find_packages(include=['ns_behave', 'ns_page_objects', 'ns_requests']),
    entry_points={"console_scripts": ["tests_replicated=ns_tests_replicated.behave_cli:cli"]},
)
