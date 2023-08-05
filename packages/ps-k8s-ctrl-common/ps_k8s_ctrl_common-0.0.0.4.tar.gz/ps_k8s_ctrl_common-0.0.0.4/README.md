# ps-k8s-ctrl-common

# What does this package do
This package is a of functions that are common to all Commercial Mobility
Kubernetes Configuration controllers

# Setup
## Clone Repo
```
# Make a copy of the repo
git clone git@git.viasat.com:Mobility-Engineering/ps-k8s-ctrl-common.git
# Load any submodules
cd ps-k8s-ctrl-common
git submodule update --init
```

## Setup version.txt file (one time only)
This repo uses automatic versioning; so you will need a version.txt file.
To create one (one time only), use the following command:
```
make version.txt
```

## Create a virtual environment (one time, unless new packages added)
```
make virt-env
```

# Generate package documentation
```
make documentation
```
The documentation is created as a web page in the pdoc folder.  Open your browser
at this URL:
    file:///(home directory for your repo)/pdoc/index.html
(eg. My repo is located at /Users/snakada/git/nebula/ps/ps-k8s-ctrl-common; so
I would open the browser at: file:///Users/snakada/git/nebual/ps/ps-k8s-ctrl-common/pdoc/index.html)
In the left column, navigate to the ps_k8s tab to find the documentation for the
PsK8s class

# How to run Unit Tests
```
source venv/bin/activate
make unit-test
```

# Run static analysis
```
make static-anaylsis
```

# Cleanup
Remove built wheel package 
```
make clean
```
Remove test docker container
```
make remove-container
```
