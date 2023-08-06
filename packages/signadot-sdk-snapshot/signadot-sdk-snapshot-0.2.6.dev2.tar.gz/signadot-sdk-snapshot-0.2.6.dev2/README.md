# Signadot Python SDK

## Installation
Install the package using the below command:
```sh
pip3 install signadot-sdk
```

Or add as a dependency to `requirements.txt` as:
```python
signadot-sdk==0.2.1
```

Then run:
```sh
pip3 install -r requirements.txt
```

## Sample Usage

```python
from pprint import pprint
import signadot_sdk

configuration = signadot_sdk.Configuration()
configuration.api_key["signadot-api-key"] = "YOUR_API_KEY"

sandboxes_api = signadot_sdk.SandboxesApi(signadot_sdk.ApiClient(configuration))
org_name = "my-org-name" # str | Signadot Org Name
fork = signadot_sdk.SandboxFork() # Create a fork object with needed customization (object not shown in detail here)

request = signadot_sdk.CreateSandboxRequest(
  name="sandbox-name",
  description="Sample sandbox created using Python SDK",
  cluster="org-cluster",
  forks=[fork])

try:
    api_response = sandboxes_api.create_new_sandbox(org_name, request)
    pprint(api_response)
except ApiException as e:
    print("Exception creating sandbox: %s\n" % e)

```