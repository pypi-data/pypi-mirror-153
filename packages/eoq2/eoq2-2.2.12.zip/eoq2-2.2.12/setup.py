import setuptools
import eoq2


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eoq2",
    version=eoq2.__version__,
    author="Bjoern Annighoefer",
    author_email="bjoern.annighoefer@ils.uni-stuttgart.de",
    description="Essential Object Query - a framework to access ecore models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/eoq/py/eoq2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyecore',
    ],
    python_requires='>=3.6',
)
