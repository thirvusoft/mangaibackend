from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in oxo/__init__.py
from oxo import __version__ as version

setup(
	name="oxo",
	version=version,
	description="oxo",
	author="thirvusoft",
	author_email="thirvusoft@yandex.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
