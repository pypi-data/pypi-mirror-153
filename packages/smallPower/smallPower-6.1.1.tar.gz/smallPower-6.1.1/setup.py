import setuptools
with open("README.md", "r", encoding="utf-8") as fh:long_description = fh.read()
setuptools.setup(
name="smallPower",
version="6.1.1",
author="Dorian Drevon",
author_email="drevondorian@gmail.com",
description="source codes and config Files to monitor small power data",
long_description=long_description,
long_description_content_type="text/markdown",
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
# packages=setuptools.find_packages(),
packages=['smallpower'],
# packages=setuptools.find_packages(exclude=["quickTest"]),
package_data={'': ['confFiles/*','confFiles/pictures/*']},
include_package_data=True,
install_requires=['dorianUtils==6.1.1'],
python_requires=">=3.8"
)
