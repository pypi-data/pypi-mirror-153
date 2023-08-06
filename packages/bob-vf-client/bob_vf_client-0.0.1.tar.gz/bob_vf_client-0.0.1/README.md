# voxelfarm client Package

This is a simple example package. You can use
[Voxelfarm PythonCookbook](https://www.voxelfarm.com/help/PythonCookbook.html/)

to write your content.


## Initialize API
This examples shows how to create a new instance of the Voxel Farm client Python API.


``` python

# Import the Voxel Farm Client Library
import voxelfarmclient

# The URL for the Voxel Farm API
vf_api_url = os.getenv('YOUR_VOXELFARM_API_URL')

# Create instance of the Voxel Farm REST API
vf = voxelfarmclient.rest(vf_api_url)

```

## Provide Credentials
This example shows how to provide credentials for API authentication.

``` python

# Set credentials
aad_app_secrets = os.getenv('AAD_APP_SECRETS')

if (aad_app_secrets!=None):
    vf.set_file_credentials(aad_app_secrets)

```

## Specify an HTTP proxy
This example shows how to specify an HTTP proxy to be used in all HTTP calls made by the API.

```
# Use a proxy to debug HTTP requests using Fiddler or similar
proxies = {
  "http": os.getenv('YOUR_PROXY_URL'),
}

# Set the proxy to debug HTTP calls
vf.set_proxy(proxies)

```

## Get CRS from project
This example shows how to retrieve the project's CRS (Coordinate Reference System).

``` python
# Get the coordinate system given project ID
result = vf.get_project_crs(project)

if not result.success:
    print(result.error_info)
    exit()
crs = result.crs

```

