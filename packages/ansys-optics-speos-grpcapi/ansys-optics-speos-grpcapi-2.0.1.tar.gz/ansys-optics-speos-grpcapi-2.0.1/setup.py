from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ansys-optics-speos-grpcapi',
    packages=find_namespace_packages(include=('ansys.*')),
    version="2.0.1",
    license='(c) 2022 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.',
    url="https://tfs.ansys.com:8443/tfs/ANSYS_Development/OPTIS_SPEOS/_git/SpeosProto",
    author="Ansys Inc.",
    author_email="support@ansys.com",
    description="Protocol Buffer structure for Speos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    install_requires=['grpcio-tools'],
)
