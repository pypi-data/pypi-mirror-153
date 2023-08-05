from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Package designed to generate REST API layer'


# Setting up
setup(
    name="REST_API_Generator",
    version=VERSION,
    author="Phani Kumar Gudepu",
    author_email="phanigudepu333@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/PhaniKumarGudepu/API_Gen",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'API', 'REST',
              'API layer', 'dummy API', 'generate', 'sanic'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
    license="MIT License"

)
