import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="avista-sensors",
    version="0.3.0",
    author="Isaac Griffith",
    author_email="grifisaa@isu.edu",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isu-avista/sensors",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
