# agilicus_api.LaunchersApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_launcher**](LaunchersApi.md#create_launcher) | **POST** /v1/launchers | Create a launcher
[**delete_launcher**](LaunchersApi.md#delete_launcher) | **DELETE** /v1/launchers/{launcher_id} | Delete a Launcher
[**get_launcher**](LaunchersApi.md#get_launcher) | **GET** /v1/launchers/{launcher_id} | Get a single launcher
[**list_launchers**](LaunchersApi.md#list_launchers) | **GET** /v1/launchers | Get all launchers
[**replace_launcher**](LaunchersApi.md#replace_launcher) | **PUT** /v1/launchers/{launcher_id} | Create or update a launcher


# **create_launcher**
> Launcher create_launcher(launcher)

Create a launcher

Create a launcher

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import launchers_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.launcher import Launcher
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
    api_instance = launchers_api.LaunchersApi(api_client)
    launcher = Launcher(
        metadata=MetadataWithId(),
        spec=LauncherSpec(
            name="name_example",
            org_id="123",
            resource_members=[
                ResourceMember(
                    id="123",
                ),
            ],
            config=LauncherConfig(
                command_path="command_path_example",
                command_arguments="command_arguments_example",
                start_in="start_in_example",
                interceptor_config=InterceptorConfig(
                    allow_list=[
                        InterceptorCommand(
                            name_exact="example.exe",
                            value_regex=".*exe",
                        ),
                    ],
                    disallow_list=[
                        InterceptorCommand(
                            name_exact="example.exe",
                            value_regex=".*exe",
                        ),
                    ],
                ),
                do_intercept=True,
                hide_console=False,
                disable_http_proxy=False,
            ),
            applications=[
                "123",
            ],
        ),
        status=LauncherStatus(
            application_services=[
                ApplicationService(
                    name="my-local-service",
                    org_id="org_id_example",
                    hostname="db.example.com",
                    ipv4_addresses=[
                        "192.0.2.1",
                    ],
                    name_resolution="static",
                    config=NetworkServiceConfig(
                        ports=[
                            NetworkPortRange(
                                protocol="tcp",
                                port=NetworkPort("5005-5010"),
                            ),
                        ],
                    ),
                    port=1,
                    protocol="tcp",
                    assignments=[
                        ApplicationServiceAssignment(
                            app_id="app_id_example",
                            environment_name="environment_name_example",
                            org_id="org_id_example",
                            expose_type="not_exposed",
                            expose_as_hostnames=[
                                Domain("expose_as_hostnames_example"),
                            ],
                        ),
                    ],
                    service_type="vpn",
                    tls_enabled=True,
                    tls_verify=True,
                    connector_id="123",
                    protocol_config=ServiceProtocolConfig(
                        http_config=ServiceHttpConfig(
                            js_injections=[
                                JSInject(
                                    script_name="script_name_example",
                                    inject_script="inject_script_example",
                                    inject_preset="inject_preset_example",
                                ),
                            ],
                            set_token_cookie=False,
                            rewrite_hostname=True,
                            rewrite_hostname_with_port=True,
                            rewrite_hostname_override="rewrite_hostname_override_example",
                        ),
                    ),
                    stats=ApplicationServiceStats(),
                ),
            ],
            file_shares=[
                FileShareService(
                    metadata=MetadataWithId(),
                    spec=FileShareServiceSpec(
                        name="share1",
                        share_name="share1",
                        org_id="123",
                        local_path="/home/agilicus/public/share1",
                        connector_id="123",
                        share_index=1,
                        transport_end_to_end_tls=True,
                        transport_base_domain="transport_base_domain_example",
                        file_level_access_permissions=False,
                        client_config=[
                            NetworkMountRuleConfig(
                                rules=ResourceRuleGroup(
                                    tags=[
                                        SelectorTag("service-desk"),
                                    ],
                                ),
                                mount=FileShareClientConfig(
                                    windows_config=FileShareClientConfigWindowsConfig(
                                        name="name_example",
                                        type="mapped_drive",
                                    ),
                                    linux_config=FileShareClientConfigLinuxConfig(
                                        path="",
                                    ),
                                    mac_config=FileShareClientConfigMacConfig(
                                        path="",
                                    ),
                                ),
                            ),
                        ],
                    ),
                    status=FileShareServiceStatus(
                        share_base_app_name="share_base_app_name_example",
                        instance_id="asdas9Gk4asdaTH",
                        instance_org_id="39ddfGAaslts8qX",
                        share_uri="https://share-4.cloud.egov.city/",
                        stats=FileShareServiceStats(),
                    ),
                ),
            ],
        ),
    ) # Launcher | 

    # example passing only required values which don't have defaults set
    try:
        # Create a launcher
        api_response = api_instance.create_launcher(launcher)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling LaunchersApi->create_launcher: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **launcher** | [**Launcher**](Launcher.md)|  |

### Return type

[**Launcher**](Launcher.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New Launcher created |  -  |
**400** | Error creating Launcher |  -  |
**409** | Launcher already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_launcher**
> delete_launcher(launcher_id)

Delete a Launcher

Delete a Launcher

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import launchers_api
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
    api_instance = launchers_api.LaunchersApi(api_client)
    launcher_id = "G" # str | Launcher unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Launcher
        api_instance.delete_launcher(launcher_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling LaunchersApi->delete_launcher: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Launcher
        api_instance.delete_launcher(launcher_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling LaunchersApi->delete_launcher: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **launcher_id** | **str**| Launcher unique identifier |
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
**204** | Launcher has been deleted |  -  |
**404** | Launcher does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_launcher**
> Launcher get_launcher(launcher_id)

Get a single launcher

Get a single launcher

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import launchers_api
from agilicus_api.model.launcher import Launcher
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
    api_instance = launchers_api.LaunchersApi(api_client)
    launcher_id = "G" # str | Launcher unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)
    expand_resource_members = False # bool | On resource requests, when True will populate member_resources with its full Resource object.  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get a single launcher
        api_response = api_instance.get_launcher(launcher_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling LaunchersApi->get_launcher: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single launcher
        api_response = api_instance.get_launcher(launcher_id, org_id=org_id, expand_resource_members=expand_resource_members)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling LaunchersApi->get_launcher: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **launcher_id** | **str**| Launcher unique identifier |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **expand_resource_members** | **bool**| On resource requests, when True will populate member_resources with its full Resource object.  | [optional] if omitted the server will use the default value of False

### Return type

[**Launcher**](Launcher.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return Launcher |  -  |
**404** | Launcher does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_launchers**
> ListLaunchersResponse list_launchers()

Get all launchers

Get all launchers

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import launchers_api
from agilicus_api.model.list_launchers_response import ListLaunchersResponse
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
    api_instance = launchers_api.LaunchersApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_id = "1234" # str | Organisation Unique identifier (optional)
    expand_resource_members = False # bool | On resource requests, when True will populate member_resources with its full Resource object.  (optional) if omitted the server will use the default value of False
    org_ids = ["q20sd0dfs3llasd0af9"] # [str] | The list of org ids to search for. Each org will be searched for independently. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all launchers
        api_response = api_instance.list_launchers(limit=limit, org_id=org_id, expand_resource_members=expand_resource_members, org_ids=org_ids)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling LaunchersApi->list_launchers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **expand_resource_members** | **bool**| On resource requests, when True will populate member_resources with its full Resource object.  | [optional] if omitted the server will use the default value of False
 **org_ids** | **[str]**| The list of org ids to search for. Each org will be searched for independently. | [optional]

### Return type

[**ListLaunchersResponse**](ListLaunchersResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | return Launchers |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_launcher**
> Launcher replace_launcher(launcher_id)

Create or update a launcher

Create or update a launcher

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import launchers_api
from agilicus_api.model.launcher import Launcher
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
    api_instance = launchers_api.LaunchersApi(api_client)
    launcher_id = "G" # str | Launcher unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)
    launcher = Launcher(
        metadata=MetadataWithId(),
        spec=LauncherSpec(
            name="name_example",
            org_id="123",
            resource_members=[
                ResourceMember(
                    id="123",
                ),
            ],
            config=LauncherConfig(
                command_path="command_path_example",
                command_arguments="command_arguments_example",
                start_in="start_in_example",
                interceptor_config=InterceptorConfig(
                    allow_list=[
                        InterceptorCommand(
                            name_exact="example.exe",
                            value_regex=".*exe",
                        ),
                    ],
                    disallow_list=[
                        InterceptorCommand(
                            name_exact="example.exe",
                            value_regex=".*exe",
                        ),
                    ],
                ),
                do_intercept=True,
                hide_console=False,
                disable_http_proxy=False,
            ),
            applications=[
                "123",
            ],
        ),
        status=LauncherStatus(
            application_services=[
                ApplicationService(
                    name="my-local-service",
                    org_id="org_id_example",
                    hostname="db.example.com",
                    ipv4_addresses=[
                        "192.0.2.1",
                    ],
                    name_resolution="static",
                    config=NetworkServiceConfig(
                        ports=[
                            NetworkPortRange(
                                protocol="tcp",
                                port=NetworkPort("5005-5010"),
                            ),
                        ],
                    ),
                    port=1,
                    protocol="tcp",
                    assignments=[
                        ApplicationServiceAssignment(
                            app_id="app_id_example",
                            environment_name="environment_name_example",
                            org_id="org_id_example",
                            expose_type="not_exposed",
                            expose_as_hostnames=[
                                Domain("expose_as_hostnames_example"),
                            ],
                        ),
                    ],
                    service_type="vpn",
                    tls_enabled=True,
                    tls_verify=True,
                    connector_id="123",
                    protocol_config=ServiceProtocolConfig(
                        http_config=ServiceHttpConfig(
                            js_injections=[
                                JSInject(
                                    script_name="script_name_example",
                                    inject_script="inject_script_example",
                                    inject_preset="inject_preset_example",
                                ),
                            ],
                            set_token_cookie=False,
                            rewrite_hostname=True,
                            rewrite_hostname_with_port=True,
                            rewrite_hostname_override="rewrite_hostname_override_example",
                        ),
                    ),
                    stats=ApplicationServiceStats(),
                ),
            ],
            file_shares=[
                FileShareService(
                    metadata=MetadataWithId(),
                    spec=FileShareServiceSpec(
                        name="share1",
                        share_name="share1",
                        org_id="123",
                        local_path="/home/agilicus/public/share1",
                        connector_id="123",
                        share_index=1,
                        transport_end_to_end_tls=True,
                        transport_base_domain="transport_base_domain_example",
                        file_level_access_permissions=False,
                        client_config=[
                            NetworkMountRuleConfig(
                                rules=ResourceRuleGroup(
                                    tags=[
                                        SelectorTag("service-desk"),
                                    ],
                                ),
                                mount=FileShareClientConfig(
                                    windows_config=FileShareClientConfigWindowsConfig(
                                        name="name_example",
                                        type="mapped_drive",
                                    ),
                                    linux_config=FileShareClientConfigLinuxConfig(
                                        path="",
                                    ),
                                    mac_config=FileShareClientConfigMacConfig(
                                        path="",
                                    ),
                                ),
                            ),
                        ],
                    ),
                    status=FileShareServiceStatus(
                        share_base_app_name="share_base_app_name_example",
                        instance_id="asdas9Gk4asdaTH",
                        instance_org_id="39ddfGAaslts8qX",
                        share_uri="https://share-4.cloud.egov.city/",
                        stats=FileShareServiceStats(),
                    ),
                ),
            ],
        ),
    ) # Launcher |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a launcher
        api_response = api_instance.replace_launcher(launcher_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling LaunchersApi->replace_launcher: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a launcher
        api_response = api_instance.replace_launcher(launcher_id, org_id=org_id, launcher=launcher)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling LaunchersApi->replace_launcher: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **launcher_id** | **str**| Launcher unique identifier |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **launcher** | [**Launcher**](Launcher.md)|  | [optional]

### Return type

[**Launcher**](Launcher.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated Launcher |  -  |
**400** | Error updating the Launcher |  -  |
**404** | Launcher does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

