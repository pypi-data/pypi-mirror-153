# python-agent
Agent to call `agent_core` using `agent_interface`
### Minimum requirements (Linux)
[install python3](https://www.python.org/downloads/)
Install pip `python3 -m pip install --user --upgrade pip`
install virtualenv `python3 -m pip install --user virtualenv`
[install nodejs](https://nodejs.org/en/download/)
## Python Packaging
### Packaging minimum requirements
Python3 `sudo apt-get install python3.x`
### Build python package
`./packaging/packaging.sh`
### Build and publish python package to pypip
`./packaging/packaging.sh -p`

# Tests
Run `./tests/test.sh`