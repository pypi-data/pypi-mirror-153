## Contents

- `batchx` package containing `bx` main application module, that offers access to the complete BatchX gRPC API from Python code.

## How to use

1. Import the library:
```
from batchx import bx
```

2. Connect to the BatchX servers (environment variables `BATCHX_ENDPOINT` and `BATCHX_TOKEN` expected)
```
bx.connect()
```

3. Instantiate service class, for example:
```
org_service = bx.OrganizationService()
```

4. Create data request, for example:
```
request = org_service.GetOrganizationRequest(organization="batchx")
```

5. Call the RPC, for example:
```
response = org_service.GetOrganization(request);
print(response)
```
