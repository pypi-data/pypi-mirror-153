import os
from setuptools import setup, find_packages


path = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(path, 'README.md')) as f:
        long_description = f.read()
except Exception as e:
    long_description = "Loading macro data based on akshare"

setup(
    name = "PPshare",
    version = "0.0.4",
    author="Lv Yiqing",
    author_email="lvyiqing121@163.com",
    description = "Loading macro data based on PPshare",
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license = "MIT Licence",
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ],

    packages =find_packages(),
    include_package_data = True,
    install_requires = ['pandas','requests','tqdm','beautifulsoup4'],
    platforms = "any",
)
