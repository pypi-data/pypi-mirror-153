# Trusted Twin Python client

Package provides easy access to Trusted Twin API using Python.

### API Reference
For Trusted Twin API documentation navigate [here](https://gitlab.com/trustedtwinpublic/api-documentation-public). 


### Installation

Using pip:

    pip install trustedtwin

From source:

    python setup.py install

### Requirements
* Python 3.6+ (CPython)

### Examples

```python
from trustedtwin import RestService

client = RestService(auth='$my_secret')

response = client.twins.create()
twin_uuid = response['creation_certificate']['uuid']
```

For code snippets please look into directory `examples`. 
