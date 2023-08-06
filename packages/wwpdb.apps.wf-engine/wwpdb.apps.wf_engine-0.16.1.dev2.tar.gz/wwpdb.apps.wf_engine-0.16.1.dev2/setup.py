# File: setup.py
# Date: 6-Oct-2018
#
# Update:
#
import re

from setuptools import find_packages
from setuptools import setup

packages = []
thisPackage = "wwpdb.apps.wf_engine"

with open("wwpdb/apps/wf_engine/__init__.py", "r") as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

setup(
    name=thisPackage,
    version=version,
    description="wwPDB workflow engine utils",
    long_description="See:  README.md",
    author="Ezra Peisach",
    author_email="ezra.peisach@rcsb.org",
    url="https://github.com/rcsb/py-wwpdb_apps_wf_engine_utils",
    #
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": []},
    #
    install_requires=[
        "psutil",
        "python-dateutil",
        "mmcif.utils",
        "wwpdb.utils.db",
        "wwpdb.utils.config",
        "wwpdb.utils.wf >= 0.5",
        "wwpdb.utils.detach",
        "wwpdb.io",
        "tabulate",
        "future",
    ],
    packages=find_packages(exclude=["wwpdb.apps.tests-wf_engine", "wwpdb.apps.wf_engine.examples"]),
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        "": ["*.md", "*.rst", "*.txt", "*.cfg"]
    },
    data_files=[
        # Data for bootstrap
        (
            "data/wf_engine/bootstrap",
            [
                "wwpdb/apps/wf_engine/wf_engine_utils/test/test-pdb-codes.ids",
                "wwpdb/apps/wf_engine/wf_engine_utils/test/test-emdb-codes.ids",
                "wwpdb/apps/wf_engine/wf_engine_utils/test/test-bmrb-codes.ids",
            ],
        ),
    ],
    #
    # These basic tests require no database services -
    test_suite="wwpdb.apps.tests-wf_engine",
    tests_require=["tox"],
    #
    # Not configured ...
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    # Added for
    command_options={"build_sphinx": {"project": ("setup.py", thisPackage), "version": ("setup.py", version), "release": ("setup.py", version)}},
    # This setting for namespace package support -
    zip_safe=False,
)
