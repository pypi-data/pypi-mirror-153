## VDR Tools for Python

This is a Python wrapper for [VDR-Tools](https://www.gitlab.com/evernym/verity/vdr-tools). It is implemented using a foreign function interface (FFI) to a native library written in Rust. Indy is the
open-source codebase behind the Sovrin network for self-sovereign digital identity.

This Python wrapper currently requires python 3.6.

Pull requests welcome!


### How to install
    pip install vdr-tools
    
Note that before you can use python wrapper you must install c-callable SDK. 
See the section "Installing" in the [VDR Tools documentation](../../README.md#installing) 
 
### How to build

- Install native "vdrtools" library:
	* Ubuntu:  [VDR Tools documentation](../../README.md#installing)
	* Windows: Currently unsupported

- Clone vdr-tools repo from https://gitlab.com/evernym/verity/vdr-tools

- Move to python wrapper directory 
```
	cd wrappers/python
```
- Create virtual env if you want

- Install dependencies with pip install

Then run

- Start local nodes pool on 127.0.0.1:9701-9708 with Docker (for now just follow same point in platform-specific instructions for libindy)

- Execute tests with pytest


### Example use
For the main workflow examples check tests in demo folder: https://gitlab.com/evernym/verity/vdr-tools/wrappers/python/tests/demo

#### Logging
The Python wrapper uses default Python logging module. So, to enable logs you need just to configure its usual way. 
Note: there is an additional log level=0 that is equal to Libindy `trace` level.