import os

import setuptools

setuptools.setup(
    name='ns_tests_replicated',
    version=os.environ.get("BUILD_VERSION", "0.0.0.dev-1"),
    dependency_links=['git+git://github.com/NarrativeScience/generic_behave/tree/reorganized_file_structure#egg=generic_behave'],
    install_requires=open("requirements.txt").readlines(),
)
