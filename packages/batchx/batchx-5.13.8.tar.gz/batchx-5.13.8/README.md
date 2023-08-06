## Contents

- `batchx` package containing `bx` main application module, that offers access to the complete BatchX gRPC API from Python code.

## How to use

```python
# Import the library
from batchx import bx

# Connect to the BatchX servers (environment variables `BATCHX_ENDPOINT` and `BATCHX_TOKEN` expected)
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
- Python protobuf messages: https://developers.google.com/protocol-buffers/docs/reference/python-generated