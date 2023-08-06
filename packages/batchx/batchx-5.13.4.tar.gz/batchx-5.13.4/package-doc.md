## Contents

- `batchx` package containing `bx` main application module, that offers access to the complete BatchX gRPC API from Python code.

## How to use

1. Import library:
```
import os;
from batchx import bx
```

2. Connect to server and provide authentication credentials:
```
bx.connect("api.batchx.io:8980", os.environ["BATCHX_TOKEN"])
```

3. Instantiate service class. For example:
```
org_service = bx.OrganizationService()
```

4. Create data request. For example:
```
request = org_service.GetOrganizationRequest(organization="batchx")
```

5. Call remote service. For example:
```
response = org_service.GetOrganization(request);
print(response)
```
