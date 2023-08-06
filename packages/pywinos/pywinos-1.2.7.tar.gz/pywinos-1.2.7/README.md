[![PyPI version](https://badge.fury.io/py/pywinos.svg)](https://badge.fury.io/py/pywinos)
[![Build Status](https://travis-ci.org/c-pher/PyWinOS.svg?branch=master)](https://travis-ci.org/c-pher/PyWinOS)
[![Coverage Status](https://coveralls.io/repos/github/c-pher/PyWinOS/badge.svg?branch=master)](https://coveralls.io/github/c-pher/PyWinOS?branch=master)

# PyWinOS
The cross-platform tool to work with remote and local Windows OS.

PyWinOS uses the Windows Remote Manager (WinRM) service. It can establish connection to a remote server based on Windows OS and execute commands:
- PowerShell
- Command line
- WMI.

It can execute commands locally using subprocess and command-line too.

For more information on WinRM, please visit [Microsoft’s WinRM site](https://docs.microsoft.com/en-us/windows/win32/winrm/portal?redirectedfrom=MSDN)
It based on [pywinrm](https://pypi.org/project/pywinrm/).

PyWinOS returns object with **exit code, stdout and sdtderr** response.

## Installation
For most users, the recommended method to install is via pip:
```cmd
pip install pywinos
```

or from source:

```cmd
python setup.py install
```

## Import
```python
from pywinos import WinOSClient
```
---
## Usage (remote server)
#### Run PowerShell:
```python
from pywinos import WinOSClient

tool = WinOSClient(host='172.16.0.126', username='administrator', password='rds123RDS', logger_enabled=True)
response = tool.run_ps(command='$PSVersionTable.PSVersion')

print(response)  
# ResponseParser(response=(0, 'Major  Minor  Build  Revision\r\n-----  -----  -----  --------\r\n5      1      17763  592', None, '$PSVersionTable.PSVersion'))
print(response.exited)  # 0
print(response.stdout)
# Major  Minor  Build  Revision
# -----  -----  -----  --------
# 5      1      17763  592

# stderr in PowerShell contains some text by default    
print(response.stderr)  # <Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04"><Ob...
print(response.ok)  # True
```

#### Run command line:
```python
from pywinos import WinOSClient

tool = WinOSClient('172.16.0.126', 'administrator', 'P@ssw0rd', logger_enabled=False)
response = tool.run_cmd(command='whoami')

print(response)  # <Response code 0, out "b'\r\nMajor  Minor  Build'", err "b''">
print(response.exited)  # 0
print(response.stdout)  # test-vm1\administrator
print(response.stderr)  # None
print(response.ok)  # True

```

## Usage (local server)
#### Run command line:
```python
from pywinos import WinOSClient

tool = WinOSClient(logger_enabled=False)
# tool = WinOSClient(host='', logger_enabled=False)
# tool = WinOSClient(host='localhost', logger_enabled=False)
# tool = WinOSClient(host='127.0.0.1', logger_enabled=False)
response = tool.run_cmd(command='whoami')

print(response)  # (0, b'mypc\\bobby\r\n', b'')
print(response.exited)  # 0
print(response.stdout)  # my_pc\bobby
print(response.stderr)  # None
print(response.ok)  # True
```

### Main low-level methods to work with local/remote Windows OS:

* run_cmd
* run_cmd_local
* run_ps
* run_ps_local

### High-level methods:

* Use `list_all_methods()` to get list of all methods.

## Changelog

### UNRELEASED

##### 1.2.7 (3.06.2022)

- log format changed according to other modules
- get_volumes() fixed to process all volumes (including service volumes without label)
- get_disks() changed. Keys are int now.
- "EntitiesQuantity" key added to bot methods
- FAQ updated

##### 1.2.6 (3.06.2022)

- Logger name changed to 'WinOSClient'
- get_disks() returns dict with disk number as key and dict with disk info as value
- get_volumes() returns dict with volume name as key and dict with volume info as value
  Both of them have optional param to get info only for specific disk/volume

##### 1.2.5 (29.04.2022)

New methods:

- .get_xml()
- .get_xml_local()

##### 1.2.4 (29.04.2022)

New method added:

- .get_disks() returns list of dict with disks info

Method updated:

- .get_volumes(): added dimension=None param. Sizes can be converted to "MB" and "GB".
  To get bytes do not set this param
- .get_volumes() extended with the "SizeUsed" field

##### 1.2.3 (28.04.2022)

New methods added:

- .get_volumes() returns list of dicts with volumes info
- .get_volumes_count() returns dict including CD-ROMs and system reserved volumes

##### 1.2.2 (22.04.2022)

- .get_process(), .get_process_local(), .get_service_file_version(), .get_service_file_version_local() raise
  ProcessLookupError if process not found
- .get_service(), .get_service_local() raise ServiceLookupError if service not found
- All method related to xmk handling marked as deprecated
- ServiceLookupError exception added
- Typos fixed

##### 1.2.1 (17.04.2022)

- updated to manage logger state

##### 1.2.0 (6.04.2022)

- External logger used
- Logger moved into class in order to have access to it after inheritance
