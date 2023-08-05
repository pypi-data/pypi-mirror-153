# agilicus_api.FilesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_file**](FilesApi.md#add_file) | **POST** /v1/files | upload a file
[**delete_file**](FilesApi.md#delete_file) | **DELETE** /v1/files/{file_id} | Delete a File
[**get_download**](FilesApi.md#get_download) | **GET** /v1/files_download/{file_id} | Download File
[**get_download_public**](FilesApi.md#get_download_public) | **GET** /v1/files_public | Download public file
[**get_file**](FilesApi.md#get_file) | **GET** /v1/files/{file_id} | Get File metadata
[**list_files**](FilesApi.md#list_files) | **GET** /v1/files | Query Files
[**replace_file**](FilesApi.md#replace_file) | **PUT** /v1/files/{file_id} | Update a file


# **add_file**
> FileSummary add_file(name, file_zip)

upload a file

Upload a file

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import files_api
from agilicus_api.model.file_name import FileName
from agilicus_api.model.file_visibility import FileVisibility
from agilicus_api.model.file_summary import FileSummary
from agilicus_api.model.storage_region import StorageRegion
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = files_api.FilesApi(api_client)
    name = FileName("Alice") # FileName | 
    file_zip = open('/path/to/file', 'rb') # file_type | The contents of the file in binary format
    org_id = "123" # str | Unique identifier (optional)
    tag = "theme" # str | A file tag (optional)
    label = "label_example" # str | A file label (optional)
    region = StorageRegion("ca") # StorageRegion |  (optional)
    visibility = FileVisibility("private") # FileVisibility |  (optional)
    md5_hash = "md5_hash_example" # str | MD5 Hash of file in base64 (optional)

    # example passing only required values which don't have defaults set
    try:
        # upload a file
        api_response = api_instance.add_file(name, file_zip)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->add_file: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # upload a file
        api_response = api_instance.add_file(name, file_zip, org_id=org_id, tag=tag, label=label, region=region, visibility=visibility, md5_hash=md5_hash)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->add_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **FileName**|  |
 **file_zip** | **file_type**| The contents of the file in binary format |
 **org_id** | **str**| Unique identifier | [optional]
 **tag** | **str**| A file tag | [optional]
 **label** | **str**| A file label | [optional]
 **region** | [**StorageRegion**](StorageRegion.md)|  | [optional]
 **visibility** | [**FileVisibility**](FileVisibility.md)|  | [optional]
 **md5_hash** | **str**| MD5 Hash of file in base64 | [optional]

### Return type

[**FileSummary**](FileSummary.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully uploaded file |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_file**
> delete_file(file_id)

Delete a File

Delete a File

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import files_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = files_api.FilesApi(api_client)
    file_id = "1234" # str | file_id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a File
        api_instance.delete_file(file_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->delete_file: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a File
        api_instance.delete_file(file_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->delete_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| file_id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | File was deleted |  -  |
**404** | File does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_download**
> file_type get_download(file_id)

Download File

Download File

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import files_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = files_api.FilesApi(api_client)
    file_id = "1234" # str | file_id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Download File
        api_response = api_instance.get_download(file_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->get_download: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Download File
        api_response = api_instance.get_download(file_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->get_download: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| file_id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

**file_type**

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Downloaded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_download_public**
> file_type get_download_public()

Download public file

Download public file

### Example

```python
import time
import agilicus_api
from agilicus_api.api import files_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)


# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = files_api.FilesApi(api_client)
    subdomain = "agilicus.cloud" # str | query based on organisation subdomain  (optional)
    label = "true" # str | Filters based on whether or not the items in the collection have the given label.  (optional)
    tag = "theme" # str | Search files based on tag (optional)
    file_in_zip = "favicon-32x32.png" # str | query based on file name inside a zip file  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Download public file
        api_response = api_instance.get_download_public(subdomain=subdomain, label=label, tag=tag, file_in_zip=file_in_zip)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->get_download_public: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subdomain** | **str**| query based on organisation subdomain  | [optional]
 **label** | **str**| Filters based on whether or not the items in the collection have the given label.  | [optional]
 **tag** | **str**| Search files based on tag | [optional]
 **file_in_zip** | **str**| query based on file name inside a zip file  | [optional]

### Return type

**file_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, application/gzip


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Downloaded |  -  |
**403** | Query not allowed |  -  |
**404** | File does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_file**
> FileSummary get_file(file_id)

Get File metadata

Get File metadata

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import files_api
from agilicus_api.model.file_summary import FileSummary
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = files_api.FilesApi(api_client)
    file_id = "1234" # str | file_id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get File metadata
        api_response = api_instance.get_file(file_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->get_file: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get File metadata
        api_response = api_instance.get_file(file_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->get_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| file_id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**FileSummary**](FileSummary.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return File by id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_files**
> ListFilesResponse list_files()

Query Files

Query Files

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import files_api
from agilicus_api.model.list_files_response import ListFilesResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = files_api.FilesApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_id = "1234" # str | Organisation Unique identifier (optional)
    user_id = "1234" # str | Query based on user id (optional)
    tag = "theme" # str | Search files based on tag (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Query Files
        api_response = api_instance.list_files(limit=limit, org_id=org_id, user_id=user_id, tag=tag)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->list_files: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **user_id** | **str**| Query based on user id | [optional]
 **tag** | **str**| Search files based on tag | [optional]

### Return type

[**ListFilesResponse**](ListFilesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return files list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_file**
> FileSummary replace_file(file_id, file)

Update a file

Update a file

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import files_api
from agilicus_api.model.file_summary import FileSummary
from agilicus_api.model.file import File
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = files_api.FilesApi(api_client)
    file_id = "1234" # str | file_id path
    file = File(
        name=FileName("Alice"),
        tag="theme",
        label="label_example",
        visibility=FileVisibility("private"),
        region=StorageRegion("ca"),
        lock=True,
    ) # File | Upload file request
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a file
        api_response = api_instance.replace_file(file_id, file)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->replace_file: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a file
        api_response = api_instance.replace_file(file_id, file, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling FilesApi->replace_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| file_id path |
 **file** | [**File**](File.md)| Upload file request |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**FileSummary**](FileSummary.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | File was updated |  -  |
**404** | File does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

