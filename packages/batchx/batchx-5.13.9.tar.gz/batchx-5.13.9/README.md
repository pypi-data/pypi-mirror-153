## Contents

The `batchx` package contains the `bx` main application module, that offers full access to the BatchX gRPC API from Python code.

## How to use

```python
# Import the module
from batchx import bx

# Connect to the BatchX servers 
# (environment variables `BATCHX_ENDPOINT` and `BATCHX_TOKEN` expected)
bx.connect()

# Instantiate service class
org_service = bx.OrganizationService()

# Create data request
request = org_service.GetOrganizationRequest(organization="batchx")

# Call the RPC
response = org_service.GetOrganization(request);

print(response)
```

## See also
- BatchX documentation: https://docs.batchx.io
- Python protobuf messages: https://developers.google.com/protocol-buffers/docs/reference/python-generated