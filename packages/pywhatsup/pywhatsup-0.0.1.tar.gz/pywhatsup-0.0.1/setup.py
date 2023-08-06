import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="pywhatsup",
    version="0.0.1",
    author="Peter Baumert",
    description="Python WhatsUp Gold API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peterbaumert/pywhatsup",
    packages=setuptools.find_packages(include=["pywhatsup"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
