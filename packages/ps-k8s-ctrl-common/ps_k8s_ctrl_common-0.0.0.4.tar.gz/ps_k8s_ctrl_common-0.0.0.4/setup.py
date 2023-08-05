import sys
import setuptools

VERSION_FILE = 'version.txt'

try:
    with open(VERSION_FILE) as version_file:
        VERSION = version_file.read().strip()
except FileNotFoundError:
    print(f'Version file "{VERSION_FILE}" not found. Use make commands instead of invoking setup.py directly')
    sys.exit(1)

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    print(f'Missing "README.md" for a long description of package.')
    sys.exit(1)

setuptools.setup(
    name="ps_k8s_ctrl_common",
    version=VERSION,
    author="Commercial Mobility Engineering",
    author_email="cm-wickedsmaht@viasat.com",
    description="Platform Services Kubernetes Controller Common Functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.viasat.com/Mobility-Engineering/ps-k8s-ctrl_common",
    license='(c) 2022 Viasat, Inc.',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
