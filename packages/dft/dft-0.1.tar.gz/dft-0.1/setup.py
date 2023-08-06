import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='dft',
    version='0.1',
    scripts=['dft'] ,
    author="Data Facade",
    author_email="info@data-facade.com",
    description="DF Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TBD",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
