# -*-coding:utf-8 -*-
import datetime
import sys

from setuptools import find_packages, setup

from maxoptics import __version__

major, minor, *_ = sys.version_info
if "develop" in sys.argv:
    assert (
        major >= 3 and minor >= 8
    ), f"Current Python ({sys.executable})\n version < 3.8"
elif "bdist_wheel" in sys.argv:
    assert (
        major == 3 and minor == 8
    ), f"Current Python ({sys.executable})\n version not 3.8"

packages = find_packages(
    ".", ("maxoptics.var.models.generators", "maxoptics.test", "test")
)
print(packages)

dt = datetime.datetime.now()

setup(
    version=__version__
    + f".{dt.month:02d}{dt.day:02d}"
    + dt.strftime(".%H%M"),
    long_description_content_type="text/markdown",
    packages=packages,
    install_requires=[
        "requests",
        "matplotlib",
        "numpy",
        "pandas",
        "pyyaml",
        "gdspy",
        "python-socketio",
        "aiohttp",
    ],
    classfiers=[
        "Development Status :: 3 -Alpha",
        "Intended Audience :: Maxoptics Developers",
        "Topic :: Software Development Kit :: Build Tools",
        "License",
        "Programming Language :: Python :: 3.8",
    ],
    package_data={
        # If any package or subpackage contains *.txt or *.rst files, include
        # them:
        "maxoptics": [
            "var/models/const/*.json",
            "var/log/.keep",
            "var/models/namespace.yml",
        ],
    },
    # include_package_data=True
    # name="maxoptics",
    # author="MaxOptics",
    # author_email="rao-jin@maxoptics.com",
    # description="MaxOptics SDK",
    # long_description=long_description,
    # platforms="Independent",
    # python_requires=">=3.8.5",
    # include_package_data=True,  # Read MANIFEST.in or not
    # url="",
    # zip_safe=False,
)
