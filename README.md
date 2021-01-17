# Simple Python SSH Key Service

> A simple python web app that generates public and private keys based on prime numbers you supply


### Usage

```python
import requests
import json


r: requests.model.Response = requests.post(
    "http://localhost:8080/generate", 
    headers={"Content-Type": "application/json"}, 
    data=json.dumps({"p": 6301, "q": 5639})
)

r.json()
```

```json
{
  "encryption_key (E)": 11,
  "modulus (N)": 35531339,
  "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMCYCAQACBAIeKksCAQsCBAGKK2MCAhidAgIWBwICCPMCAhIFAgIRcA==\n-----END RSA PRIVATE KEY-----",
  "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABCwAAAAQCHipL"
}
```

# Endpoints
- `generate` ✅
- `encrypt` (WIP)
- `decrypt` (WIP)


### todo
- tests
- add endpoint link
