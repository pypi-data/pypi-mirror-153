import os
import json
from setuptools import setup, find_packages

pkg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "package.json")
params = json.load(open(pkg))

setup(
    name=params["name"],
    version=params["version"],
    description=params["description"],
    long_description=open("README.md", "rt").read(),
    long_description_content_type="text/markdown",
    license=open("LICENSE", "rt").read(),
    zip_safe=False,
    entry_points={"console_scripts": ["emptyfile=emptyfile.__main__:main"]},
    packages=find_packages(),
    requires=(),
    include_package_data=True
)
