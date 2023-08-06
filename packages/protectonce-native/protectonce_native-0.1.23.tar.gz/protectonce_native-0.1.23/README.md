# agent_interface
#### Interface to call agent_core from different run times other than nodejs
## Compilation
### Build Minimum requirements (Linux)
Install cmake `apt-get install -y cmake`
## Compilation
Run script `./build.sh`
## Python Packaging
### Packaging minimum requirements
Python3 `sudo apt-get install python3.x`
nvm needs to be installed 
How to install nvm? refer this link https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-20-04
### Build python package
`./packaging/packaging.sh`
### Build and publish python package to pypip
`./packaging/packaging.sh -p`
# Testing
#### Unit tests and Component tests
### Build Minimum requirement for Unit and Component tests
[Install docker](https://docs.docker.com/engine/install/) , [install nodejs](https://nodejs.org/en/download/)
### Compilation and Execution
Run both tests `./tests/test.sh`
## Unit Tests
Testing `agent_interface` with mocked `agent_core` 
### Compilation and Execution
Run `./tests/test.sh -u`
### Where is test report?
HTML test report is generated on path
`/tests/unit/out/reports/Unit_test_report.html`
### Run Unit tests on list of raw docker images
Run `./tests/unit/docker_test.sh`
## Component tests
Testing `agent_interface` and `agent_core` with mocked `po_backend_mock`
### Compilation and Execution
Run `./tests/test.sh -c`
### Where are test reports?
HTML test report is generated on path
`/tests/component/out/reports/Component_test_report.html`