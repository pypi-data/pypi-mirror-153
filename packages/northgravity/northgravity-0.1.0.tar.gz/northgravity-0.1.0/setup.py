import os

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=os.getenv('LIBRARY_NAME'),
    version=os.getenv('LIBRARY_VERSION'),
    author=os.getenv('LIBRARY_AUTHOR'),
    author_email=os.getenv('LIBRARY_AUTHOR_EMAIL'),
    description=os.getenv('SETUP_DESCRIPTION'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=os.getenv('COMPANY_HOMEPAGE'),
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent"
                 ],
    install_requires = [
        'requests>=2.27.1',
        'urllib3>=1.26.9'
    ],
    python_requires='>=3.6',
)
