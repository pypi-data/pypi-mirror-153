import setuptools

with open("README.md","r") as fh:
    long_description=fh.read()


setuptools.setup(
    name="statistique",
    version="0.0.1",
    author="Factis-Nuza",
    description="Librarie pour le calculs statistiques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
    py_modules=["statistique"],
    package_dir={'':'statistique/src'},
    install_requires=[]
)