from setuptools import setup,find_packages

setup(
    name = "chemaphy",
    version = "0.6",
    description = "Package for Scientific calculation",
    long_description = "For more info, check mine github repository",
    author = "Sahil Rajwar",
    author_email = "justsahilrajwar2004@gmail.com",
    packages = ["chemaphy"],
    license = "MIT",
    install_requires = ["numpy","trigo","pandas"],
    url = "https://github.com/Sahil-Rajwar-2004/chemaphy",
    keywords = ["calculator","scipy","calc"],
    classifiers = [
    "Programming Language :: Python :: 3",
    "Intended Audience :: Education",
    "Operating System :: OS Independent",
    ]

)
