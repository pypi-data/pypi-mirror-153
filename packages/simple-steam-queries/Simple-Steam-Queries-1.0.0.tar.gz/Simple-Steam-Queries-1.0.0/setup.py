import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Simple-Steam-Queries",
    version="1.0.0",
    author="Giannis Spentzas",
    author_email="gspentzas1991@gmail.com",
    description="A python module that allows you to easily run Steam Master Server Query Protocol queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gspentzas1991/Simple-Steam-Queries",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)