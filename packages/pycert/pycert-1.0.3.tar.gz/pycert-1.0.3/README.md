[![PyPI version](https://badge.fury.io/py/pycert.svg)](https://badge.fury.io/py/pycert)
[![Build Status](https://app.travis-ci.com/c-pher/certificate.svg?branch=master)](https://app.travis-ci.com/c-pher/certificate)

# Certificate

The cross-platform tool to get certificate info (including self-signed).

## Installation

For most users, the recommended method to install is via pip:

```cmd
pip install pycert
```

## Import

```python
from pycert import CertClient
```

---

## Usage

#### Command from usual user:

```python
from pycert import CertClient

client = CertClient(host="172.16.0.124")
print(client.get_all_info())

```

```python
from pprint import pprint
from pycert import CertClient

cert = CertClient('pypi.org')

pprint(cert.get_all_info())

```

```json
{
  "version": "v3",
  "valid_from": "2021-10-22T18:41:11",
  "valid_to": "2022-11-23T18:41:10",
  "is_valid": true,
  "is_self_signed": false,
  "issuer": {
    "C": "BE",
    "O": "GlobalSign nv-sa",
    "CN": "GlobalSign Atlas R3 DV TLS CA H2 2021"
  },
  "subject": {
    "CN": "www.python.org"
  },
  "signature_algorithm": "sha256",
  "serial_number": "1B7C6CD03E8E071BE48C2B1A7994075",
  "alternative_name": [
    "DNS:www.python.org",
    "DNS:*.python.org",
    "DNS:docs.python.org",
    "DNS:downloads.python.org",
    "DNS:pypi.python.org"
  ],
  "fingerprint": "CE1F8748D2DA0265B329F1DFD70047DCEF6CD8FB"
}
```

## Useful links

- [RFC3280](https://datatracker.ietf.org/doc/html/rfc3280)
- [OpenSSL cheatsheet](https://megamorf.gitlab.io/cheat-sheets/openssl/)

## Changelog:

##### unreleased

##### 1.0.3 (4.06.2022)

- Log name changed to `CertClient`
- Log format changed according other modules

##### 1.0.2 (17.04.2022)

- External logger added

##### 1.0.1 (14.12.2021)

- refactored "get_all_info": not it gets issuer and subject dynamically
- get_serial_number: returns upper hexadecimal without first bit now
- is_self_signed: preliminary method added (can be changed in future)
- get_all_methods fixed: now it returns CertClient methods
- get_alt_name refactored to get extension using oid

##### 1.0.0 (8.12.2021)

- New method added: get_fingerprint()
- get_all_info() extended with thumbprint, added params (fp_brief=True, signature_algorithm_brief=True)
- get_signature_algorithm() updated to return full or brief signature info

##### 0.0.12 (30.11.2021)

- example added

##### 0.0.1 (30.11.2021)

- initial commit