import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="storck_client",
    author_email="mmajewsk@cern.ch",
    description="A client library for storck database system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/velo-calibration-software/storck_client",
    project_urls={
        "Bug Tracker": "https://gitlab.cern.ch/velo-calibration-software/storck_client/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    py_modules = ['storck_client', "storck_sync", "storck_upload", '__main__'],
    python_requires=">=3.6",
    install_requires=["requests>=2.25.1"],
    version='0.1.1',


)
