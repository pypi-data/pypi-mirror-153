# OpenDataLab Python SDK


[![Downloads](https://pepy.tech/badge/opendatahub/month)](https://pepy.tech/project/opendatahub)
[![PyPI](https://img.shields.io/pypi/v/opendatahub)](https://pypi.org/project/opendatahub/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/opendatahub)](https://pypi.org/project/opendatahub/)

---

**IMPORTANT**: OpenDataHub SDK status: WIP, which will not ensure the necessary compatibility of OpenAPI and SDK. As a result, please use the SDK with released version later.  

**Please wait for the released version!!!**

---

OpenDataHub Python SDK is a python library to access [Opendatalab](https://opendatalab.com/)
and use open datasets.  
It provides:

-   A pythonic way to access opendatalab resources by Opendatalab OpenAPI.
-   An convient CLI tool `odl` (Opendatalab for short) to access open datasets.
-   Rich information about the open datasets.

## Installation

```console
pip3 install opendatahub
```

## Usage:

An **account** is needed to access to opendatalab service.
Please visit [offical websit](https://opendatalab.com/register) to get the account username and password first.

### Login
login with opendatalab username and password 
```cmd
odl login -u aaa@email.com -p ****
```
or 
```python
from opendatahub import ODL
odl = ODL.auth(username, pasword)

```

### Logout
logout current opendatalab account 
```cmd
odl logout
```
or 
```python
from opendatahub import ODL
odl.logout()
```

### ls 
list all dataset by offset, limit
```cmd
odl ls 
```
or
```python
from opendatahub import ODL
odl.list_datasets()
```

### info
show dataset info in json format
```cmd
odl info coco
```
or
```python
from opendatahub import ODL
odl.get_info()
```

### search
search dataset by name
```cmd
odl search coco 
```
or
```python
from opendatahub import ODL
odl.search('coco')
```

### download
download dataset into local path
```cmd
odl download --name coco --root /home/XXX/coco 
```
or
```python
from opendatahub import ODL
odl.download(name='coco', root='/home/XXX/coco ' )
``` 

## Documentation

More information can be found on the [documentation site](https://opendatalab.com/docs)