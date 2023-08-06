from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fp:
    install_requires = fp.read()

setup(
    name="snelstart",
    version="0.1.0",
    author="Zypp",
    author_email="hello@zypp.io",
    description="Package for pulling datasets using the Snelstart API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="python, snelstart, API",
    url="https://github.com/zypp-io/snelstart",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    project_urls={
        "Bug Reports": "https://github.com/zypp-io/snelstart/issues",
        "Source": "https://github.com/zypp-io/snelstart",
    },
)
