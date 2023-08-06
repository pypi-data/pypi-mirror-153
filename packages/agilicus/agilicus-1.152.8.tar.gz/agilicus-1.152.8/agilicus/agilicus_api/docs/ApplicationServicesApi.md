# agilicus_api.ApplicationServicesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_application_service**](ApplicationServicesApi.md#create_application_service) | **POST** /v2/application_services | Create an ApplicationService
[**create_application_service_token**](ApplicationServicesApi.md#create_application_service_token) | **POST** /v2/application_services/{app_service_id}/token | create a token for an application service
[**create_client_configuration**](ApplicationServicesApi.md#create_client_configuration) | **POST** /v1/desktop_resources/{resource_id}/client_configurations | Create a client configuration
[**create_desktop_resource**](ApplicationServicesApi.md#create_desktop_resource) | **POST** /v1/desktop_resources | Create a DesktopResource
[**create_file_share_service**](ApplicationServicesApi.md#create_file_share_service) | **POST** /v1/file_share_services | Create an FileShareService
[**create_service_forwarder**](ApplicationServicesApi.md#create_service_forwarder) | **POST** /v1/service_forwarders | Create an ServiceForwarder
[**delete_application_service**](ApplicationServicesApi.md#delete_application_service) | **DELETE** /v2/application_services/{app_service_id} | Remove an ApplicationService
[**delete_desktop_resource**](ApplicationServicesApi.md#delete_desktop_resource) | **DELETE** /v1/desktop_resources/{resource_id} | Remove a DesktopResource
[**delete_file_share_service**](ApplicationServicesApi.md#delete_file_share_service) | **DELETE** /v1/file_share_services/{file_share_service_id} | Remove an FileShareService
[**delete_service_forwarder**](ApplicationServicesApi.md#delete_service_forwarder) | **DELETE** /v1/service_forwarders/{service_forwarder_id} | Remove an ServiceForwarder
[**get_application_service**](ApplicationServicesApi.md#get_application_service) | **GET** /v2/application_services/{app_service_id} | Get a single ApplicationService
[**get_application_service_usage_metrics**](ApplicationServicesApi.md#get_application_service_usage_metrics) | **GET** /v2/application_services/usage_metrics | Get application service metrics
[**get_desktop_resource**](ApplicationServicesApi.md#get_desktop_resource) | **GET** /v1/desktop_resources/{resource_id} | Get a single DesktopResource
[**get_file_share_service**](ApplicationServicesApi.md#get_file_share_service) | **GET** /v1/file_share_services/{file_share_service_id} | Get a single FileShareService
[**get_file_share_usage_metrics**](ApplicationServicesApi.md#get_file_share_usage_metrics) | **GET** /v1/file_share_services/usage_metrics | Get file share service metrics
[**get_service_forwarder**](ApplicationServicesApi.md#get_service_forwarder) | **GET** /v1/service_forwarders/{service_forwarder_id} | Get a single ServiceForwarder
[**list_application_services**](ApplicationServicesApi.md#list_application_services) | **GET** /v2/application_services | Get a subset of the ApplicationServices
[**list_desktop_resources**](ApplicationServicesApi.md#list_desktop_resources) | **GET** /v1/desktop_resources | Get a subset of the DesktopResource objects.
[**list_file_share_services**](ApplicationServicesApi.md#list_file_share_services) | **GET** /v1/file_share_services | Get a subset of the FileShareServices
[**list_service_forwarders**](ApplicationServicesApi.md#list_service_forwarders) | **GET** /v1/service_forwarders | Get a subset of the ServiceForwarder objects
[**replace_application_service**](ApplicationServicesApi.md#replace_application_service) | **PUT** /v2/application_services/{app_service_id} | Create or update an Application Service.
[**replace_desktop_resource**](ApplicationServicesApi.md#replace_desktop_resource) | **PUT** /v1/desktop_resources/{resource_id} | Create or update a DesktopResource.
[**replace_file_share_service**](ApplicationServicesApi.md#replace_file_share_service) | **PUT** /v1/file_share_services/{file_share_service_id} | Create or update an FileShareService.
[**replace_service_forwarder**](ApplicationServicesApi.md#replace_service_forwarder) | **PUT** /v1/service_forwarders/{service_forwarder_id} | Create or update an ServiceForwarder.


# **create_application_service**
> ApplicationService create_application_service(application_service)

Create an ApplicationService

It is expected that owners for an organisation will provide connectivity to an ApplicationService by defining one here, then adding a reference to an Application's Environment in the ApplicationService's `assignments` list. To see the list of ApplicationServices for which a given Application Environment has access, see that Environment's read only `applications_services` list. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.application_service import ApplicationService
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    application_service = ApplicationService(
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
    ) # ApplicationService | 

    # example passing only required values which don't have defaults set
    try:
        # Create an ApplicationService
        api_response = api_instance.create_application_service(application_service)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_application_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_service** | [**ApplicationService**](ApplicationService.md)|  |

### Return type

[**ApplicationService**](ApplicationService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New ApplicationService created |  -  |
**409** | An ApplicationService with the same name already exists for this organisation. The existing ApplicationService is returned.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_application_service_token**
> RawToken create_application_service_token(app_service_id, org_id)

create a token for an application service

Create a token for an application service

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.raw_token import RawToken
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    app_service_id = "G" # str | Application Service unique identifier
    org_id = "G" # str | Organisation unique identifier

    # example passing only required values which don't have defaults set
    try:
        # create a token for an application service
        api_response = api_instance.create_application_service_token(app_service_id, org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_application_service_token: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier |
 **org_id** | **str**| Organisation unique identifier |

### Return type

[**RawToken**](RawToken.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | A token has been created |  -  |
**404** | The ApplicationService does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_client_configuration**
> DesktopClientConfiguration create_client_configuration(resource_id)

Create a client configuration

Create a client configuration file. This file may be downloaded and used by the appropriate client to connect to the DesktopResource. If you provide the id of user who wants to connect, the file will contain credentials which may be used to prove their authorization to access the DesktopResource. The DesktopClientConfiguration is not stored in the system. Subsequent calls to create a new DesktopClientConfiguration will lead to a new one being generated. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.desktop_client_configuration import DesktopClientConfiguration
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    resource_id = "X1Isks5kslds945" # str | The id of the resource to access
    desktop_client_configuration = DesktopClientConfiguration(
        user_id="L5JX4aSd6aM",
        org_id="org_id_example",
        generated_config=DesktopClientGeneratedConfiguration(
            desktop_resource_id="desktop_resource_id_example",
            configuration_file='YQ==',
            configuration_file_media_type="application/rdp",
        ),
    ) # DesktopClientConfiguration |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create a client configuration
        api_response = api_instance.create_client_configuration(resource_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_client_configuration: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create a client configuration
        api_response = api_instance.create_client_configuration(resource_id, desktop_client_configuration=desktop_client_configuration)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_client_configuration: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**| The id of the resource to access |
 **desktop_client_configuration** | [**DesktopClientConfiguration**](DesktopClientConfiguration.md)|  | [optional]

### Return type

[**DesktopClientConfiguration**](DesktopClientConfiguration.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The DesktopClientConfiguration was succesfully created.  |  -  |
**400** | A problem was encounted creating the DesktopClientConfiguration. Often this can happen because the request was malformed, but it could also happen because the system failed to retrieve credentials for the requested user.  |  -  |
**404** | The DesktopResource does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_desktop_resource**
> DesktopResource create_desktop_resource(desktop_resource)

Create a DesktopResource

Administrators for an organisation can allow remote connectivity to a desktop by creating a DesktopResource using this endpoint. Make sure to expose the DesktopResource through a connector by setting the `connector_id`. You can create multiple DesktopResource objects. for a given desktop. The name of the DesktopResource uniquely identifies it. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.desktop_resource import DesktopResource
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    desktop_resource = DesktopResource(
        metadata=MetadataWithId(),
        spec=DesktopResourceSpec(
            name="my-desktop-1",
            address="address_example",
            config=NetworkServiceConfig(
                ports=[
                    NetworkPortRange(
                        protocol="tcp",
                        port=NetworkPort("5005-5010"),
                    ),
                ],
            ),
            desktop_type="rdp",
            session_type="user",
            org_id="123",
            connector_id="123",
            name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
            connection_info=DesktopConnectionInfo(
                vnc_connection_info=VNCConnectionInfo(
                    password_authentication_info=VNCPasswordAuthentication(
                        read_write_password="read_write_password_example",
                        read_only_password="read_only_password_example",
                    ),
                ),
            ),
        ),
        status=DesktopResourceStatus(
            gateway_uri="https://desktops.cloud.egov.city/remoteDesktopGateway/",
            stats=DesktopResourceStats(),
        ),
    ) # DesktopResource | 

    # example passing only required values which don't have defaults set
    try:
        # Create a DesktopResource
        api_response = api_instance.create_desktop_resource(desktop_resource)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_desktop_resource: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **desktop_resource** | [**DesktopResource**](DesktopResource.md)|  |

### Return type

[**DesktopResource**](DesktopResource.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New DesktopResource created |  -  |
**409** | A DesktopResource with the same name already exists for this organisation. The existing DesktopResource is returned.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_file_share_service**
> FileShareService create_file_share_service(file_share_service)

Create an FileShareService

It is expected that owners for an organisation will provide connectivity to an FileShareService by defining one here, then adding a reference to an Application's Environment in the FileShareService's `assignments` list. To see the list of FileShareServices for which a given Application Environment has access, see that Environment's read only `applications_services` list. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.file_share_service import FileShareService
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    file_share_service = FileShareService(
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
    ) # FileShareService | 

    # example passing only required values which don't have defaults set
    try:
        # Create an FileShareService
        api_response = api_instance.create_file_share_service(file_share_service)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_file_share_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_share_service** | [**FileShareService**](FileShareService.md)|  |

### Return type

[**FileShareService**](FileShareService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New FileShareService created |  -  |
**409** | An FileShareService with the same name already exists for this organisation. The existing FileShareService is returned.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_service_forwarder**
> ServiceForwarder create_service_forwarder(service_forwarder)

Create an ServiceForwarder

Create an ServiceForwarder

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.service_forwarder import ServiceForwarder
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    service_forwarder = ServiceForwarder(
        metadata=MetadataWithId(),
        spec=ServiceForwarderSpec(
            name="name_example",
            org_id="org_id_example",
            bind_address="localhost",
            port=1,
            protocol="tcp",
            application_service_id="application_service_id_example",
            connector_id="123",
        ),
        status=ServiceForwarderStatus(
            connection_uri="connection_uri_example",
            application_service=ApplicationService(
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
            stats=ServiceForwarderStats(),
        ),
    ) # ServiceForwarder | 

    # example passing only required values which don't have defaults set
    try:
        # Create an ServiceForwarder
        api_response = api_instance.create_service_forwarder(service_forwarder)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_service_forwarder: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_forwarder** | [**ServiceForwarder**](ServiceForwarder.md)|  |

### Return type

[**ServiceForwarder**](ServiceForwarder.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New ServiceForwarder created |  -  |
**409** | An ServiceForwarder with the same name already exists for this organisation. The existing ServiceForwarder is returned.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_application_service**
> delete_application_service(app_service_id, org_id)

Remove an ApplicationService

Remove an ApplicationService

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    app_service_id = "G" # str | Application Service unique identifier
    org_id = "G" # str | Organisation unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Remove an ApplicationService
        api_instance.delete_application_service(app_service_id, org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_application_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier |
 **org_id** | **str**| Organisation unique identifier |

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
**204** | Application Service was deleted |  -  |
**404** | Application Service does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_desktop_resource**
> delete_desktop_resource(resource_id)

Remove a DesktopResource

Remove a DesktopResource. After removal, users will no longer be able to access the DesktopResource. Existing connections to the DesktopResource may persist for some time afterwards. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.error_message import ErrorMessage
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    resource_id = "X1Isks5kslds945" # str | The id of the resource to access
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Remove a DesktopResource
        api_instance.delete_desktop_resource(resource_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_desktop_resource: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Remove a DesktopResource
        api_instance.delete_desktop_resource(resource_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_desktop_resource: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**| The id of the resource to access |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | DesktopResource was deleted |  -  |
**404** | DesktopResource does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_file_share_service**
> delete_file_share_service(file_share_service_id)

Remove an FileShareService

Remove an FileShareService

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    file_share_service_id = "G" # str | FileShareService unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Remove an FileShareService
        api_instance.delete_file_share_service(file_share_service_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_file_share_service: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Remove an FileShareService
        api_instance.delete_file_share_service(file_share_service_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_file_share_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_share_service_id** | **str**| FileShareService unique identifier |
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
**204** | FileShareService was deleted |  -  |
**404** | FileShareService does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_service_forwarder**
> delete_service_forwarder(service_forwarder_id)

Remove an ServiceForwarder

Remove an ServiceForwarder

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    service_forwarder_id = "G" # str | Service Forwarder unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Remove an ServiceForwarder
        api_instance.delete_service_forwarder(service_forwarder_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_service_forwarder: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Remove an ServiceForwarder
        api_instance.delete_service_forwarder(service_forwarder_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_service_forwarder: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_forwarder_id** | **str**| Service Forwarder unique identifier |
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
**204** | IngresssService was deleted |  -  |
**404** | IngresssService does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_application_service**
> ApplicationService get_application_service(app_service_id, org_id)

Get a single ApplicationService

Get a single ApplicationService

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.application_service import ApplicationService
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    app_service_id = "G" # str | Application Service unique identifier
    org_id = "G" # str | Organisation unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Get a single ApplicationService
        api_response = api_instance.get_application_service(app_service_id, org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_application_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier |
 **org_id** | **str**| Organisation unique identifier |

### Return type

[**ApplicationService**](ApplicationService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ApplicationService was found. |  -  |
**404** | The ApplicationService does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_application_service_usage_metrics**
> UsageMetric get_application_service_usage_metrics(org_id)

Get application service metrics

Retrieves all application service metrics related to the org_id. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.usage_metric import UsageMetric
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Get application service metrics
        api_response = api_instance.get_application_service_usage_metrics(org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_application_service_usage_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |

### Return type

[**UsageMetric**](UsageMetric.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return application service Usage metrics |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_desktop_resource**
> DesktopResource get_desktop_resource(resource_id)

Get a single DesktopResource

Get the details of a single DesktopResource. Specify the id of the organisation which owns this resource to ensure you have permission. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.desktop_resource import DesktopResource
from agilicus_api.model.error_message import ErrorMessage
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    resource_id = "X1Isks5kslds945" # str | The id of the resource to access
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a single DesktopResource
        api_response = api_instance.get_desktop_resource(resource_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_desktop_resource: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single DesktopResource
        api_response = api_instance.get_desktop_resource(resource_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_desktop_resource: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**| The id of the resource to access |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**DesktopResource**](DesktopResource.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The DesktopResource was found. |  -  |
**404** | The DesktopResource does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_file_share_service**
> FileShareService get_file_share_service(file_share_service_id)

Get a single FileShareService

Get a single FileShareService

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.file_share_service import FileShareService
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    file_share_service_id = "G" # str | FileShareService unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a single FileShareService
        api_response = api_instance.get_file_share_service(file_share_service_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_file_share_service: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single FileShareService
        api_response = api_instance.get_file_share_service(file_share_service_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_file_share_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_share_service_id** | **str**| FileShareService unique identifier |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**FileShareService**](FileShareService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The FileShareService was found. |  -  |
**404** | The FileShareService does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_file_share_usage_metrics**
> UsageMetric get_file_share_usage_metrics(org_id)

Get file share service metrics

Retrieves all file share service metrics related to the org_id. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.usage_metric import UsageMetric
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Get file share service metrics
        api_response = api_instance.get_file_share_usage_metrics(org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_file_share_usage_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |

### Return type

[**UsageMetric**](UsageMetric.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return file share services Usage metrics |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_service_forwarder**
> ServiceForwarder get_service_forwarder(service_forwarder_id)

Get a single ServiceForwarder

Get a single ServiceForwarder

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.service_forwarder import ServiceForwarder
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    service_forwarder_id = "G" # str | Service Forwarder unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a single ServiceForwarder
        api_response = api_instance.get_service_forwarder(service_forwarder_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_service_forwarder: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single ServiceForwarder
        api_response = api_instance.get_service_forwarder(service_forwarder_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_service_forwarder: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_forwarder_id** | **str**| Service Forwarder unique identifier |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**ServiceForwarder**](ServiceForwarder.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ServiceForwarder was found. |  -  |
**404** | The ServiceForwarder does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_application_services**
> ListApplicationServicesResponse list_application_services()

Get a subset of the ApplicationServices

Retrieves all ApplicationServices owned by the Organisation.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.list_application_services_response import ListApplicationServicesResponse
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    updated_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | query since updated (optional)
    protocol_type = "ip" # str | ApplicationService protocol type (optional)
    protocol_type_list = [
        "ip",
    ] # [str] | list of application service protocol types to query for (optional)
    name = "service1" # str | Query the service by name (optional)
    hostname = "hostname_example" # str | ApplicationService hostname query lookup (optional)
    hostname_or_service_name = "hostname_or_service_name_example" # str | Perform a query based on the following       (hostname == hostname_or_service_name)            OR       (servicename == hostname_or_service_name AND hostname == localhost)  (optional)
    port = 1 # int | ApplicationService port query lookup (optional)
    show_status = True # bool | Whether the return value should include the status for included objects. If false the query may run faster but will not include status information.  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a subset of the ApplicationServices
        api_response = api_instance.list_application_services(org_id=org_id, updated_since=updated_since, protocol_type=protocol_type, protocol_type_list=protocol_type_list, name=name, hostname=hostname, hostname_or_service_name=hostname_or_service_name, port=port, show_status=show_status)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->list_application_services: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **updated_since** | **datetime**| query since updated | [optional]
 **protocol_type** | **str**| ApplicationService protocol type | [optional]
 **protocol_type_list** | **[str]**| list of application service protocol types to query for | [optional]
 **name** | **str**| Query the service by name | [optional]
 **hostname** | **str**| ApplicationService hostname query lookup | [optional]
 **hostname_or_service_name** | **str**| Perform a query based on the following       (hostname &#x3D;&#x3D; hostname_or_service_name)            OR       (servicename &#x3D;&#x3D; hostname_or_service_name AND hostname &#x3D;&#x3D; localhost)  | [optional]
 **port** | **int**| ApplicationService port query lookup | [optional]
 **show_status** | **bool**| Whether the return value should include the status for included objects. If false the query may run faster but will not include status information.  | [optional] if omitted the server will use the default value of False

### Return type

[**ListApplicationServicesResponse**](ListApplicationServicesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of retrieved ApplicationServices |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_desktop_resources**
> ListDesktopResourcesResponse list_desktop_resources()

Get a subset of the DesktopResource objects.

Retrieves DesktopResource objects owned by the Organisation.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.list_desktop_resources_response import ListDesktopResourcesResponse
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    name = "my-application" # str | The name of the resource to query for (optional)
    connector_id = "1234" # str | connector id in query (optional)
    updated_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | query since updated (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_ids = ["q20sd0dfs3llasd0af9"] # [str] | The list of org ids to search for. Each org will be searched for independently. (optional)
    resource_id = "owner" # str | The id of the resource to query for (optional)
    page_at_id = "foo@example.com" # str | Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_id` field from the list response.  (optional)
    name_slug = "smy-application1234" # str | The slug of the resource to query for (optional)
    desktop_type = "rdp" # str | The type of desktop search for. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a subset of the DesktopResource objects.
        api_response = api_instance.list_desktop_resources(org_id=org_id, name=name, connector_id=connector_id, updated_since=updated_since, limit=limit, org_ids=org_ids, resource_id=resource_id, page_at_id=page_at_id, name_slug=name_slug, desktop_type=desktop_type)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->list_desktop_resources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **name** | **str**| The name of the resource to query for | [optional]
 **connector_id** | **str**| connector id in query | [optional]
 **updated_since** | **datetime**| query since updated | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_ids** | **[str]**| The list of org ids to search for. Each org will be searched for independently. | [optional]
 **resource_id** | **str**| The id of the resource to query for | [optional]
 **page_at_id** | **str**| Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the &#x60;page_at_id&#x60; field from the list response.  | [optional]
 **name_slug** | **str**| The slug of the resource to query for | [optional]
 **desktop_type** | **str**| The type of desktop search for. | [optional]

### Return type

[**ListDesktopResourcesResponse**](ListDesktopResourcesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of retrieved DesktopResource objects. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_file_share_services**
> ListFileShareServicesResponse list_file_share_services()

Get a subset of the FileShareServices

Retrieves all FileShareServices owned by the Organisation.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.list_file_share_services_response import ListFileShareServicesResponse
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    name = "service1" # str | Query the service by name (optional)
    connector_id = "1234" # str | connector id in query (optional)
    updated_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | query since updated (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_ids = ["q20sd0dfs3llasd0af9"] # [str] | The list of org ids to search for. Each org will be searched for independently. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a subset of the FileShareServices
        api_response = api_instance.list_file_share_services(org_id=org_id, name=name, connector_id=connector_id, updated_since=updated_since, limit=limit, org_ids=org_ids)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->list_file_share_services: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **name** | **str**| Query the service by name | [optional]
 **connector_id** | **str**| connector id in query | [optional]
 **updated_since** | **datetime**| query since updated | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_ids** | **[str]**| The list of org ids to search for. Each org will be searched for independently. | [optional]

### Return type

[**ListFileShareServicesResponse**](ListFileShareServicesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of retrieved FileShareServices |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_service_forwarders**
> ListServiceForwardersResponse list_service_forwarders()

Get a subset of the ServiceForwarder objects

Retrieves all ServiceForwarder objects owned by the Organisation.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.list_service_forwarders_response import ListServiceForwardersResponse
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    name = "service1" # str | Query the service by name (optional)
    app_service_id = "G" # str | Application Service unique identifier (optional)
    connector_id = "1234" # str | connector id in query (optional)
    app_service_connector_id = "1234" # str | application service connector id in query (optional)
    updated_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | query since updated (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_ids = ["q20sd0dfs3llasd0af9"] # [str] | The list of org ids to search for. Each org will be searched for independently. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a subset of the ServiceForwarder objects
        api_response = api_instance.list_service_forwarders(org_id=org_id, name=name, app_service_id=app_service_id, connector_id=connector_id, app_service_connector_id=app_service_connector_id, updated_since=updated_since, limit=limit, org_ids=org_ids)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->list_service_forwarders: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **name** | **str**| Query the service by name | [optional]
 **app_service_id** | **str**| Application Service unique identifier | [optional]
 **connector_id** | **str**| connector id in query | [optional]
 **app_service_connector_id** | **str**| application service connector id in query | [optional]
 **updated_since** | **datetime**| query since updated | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_ids** | **[str]**| The list of org ids to search for. Each org will be searched for independently. | [optional]

### Return type

[**ListServiceForwardersResponse**](ListServiceForwardersResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of retrieved ServiceForwarder objects |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_application_service**
> ApplicationService replace_application_service(app_service_id)

Create or update an Application Service.

Create or update an Application Service.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.application_service import ApplicationService
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    app_service_id = "G" # str | Application Service unique identifier
    application_service = ApplicationService(
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
    ) # ApplicationService |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update an Application Service.
        api_response = api_instance.replace_application_service(app_service_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_application_service: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update an Application Service.
        api_response = api_instance.replace_application_service(app_service_id, application_service=application_service)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_application_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier |
 **application_service** | [**ApplicationService**](ApplicationService.md)|  | [optional]

### Return type

[**ApplicationService**](ApplicationService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ApplicationService was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | Application Service does not exist. |  -  |
**409** | The provided Application Service conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_desktop_resource**
> DesktopResource replace_desktop_resource(resource_id)

Create or update a DesktopResource.

Create or update a DesktopResource.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.desktop_resource import DesktopResource
from agilicus_api.model.error_message import ErrorMessage
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    resource_id = "X1Isks5kslds945" # str | The id of the resource to access
    desktop_resource = DesktopResource(
        metadata=MetadataWithId(),
        spec=DesktopResourceSpec(
            name="my-desktop-1",
            address="address_example",
            config=NetworkServiceConfig(
                ports=[
                    NetworkPortRange(
                        protocol="tcp",
                        port=NetworkPort("5005-5010"),
                    ),
                ],
            ),
            desktop_type="rdp",
            session_type="user",
            org_id="123",
            connector_id="123",
            name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
            connection_info=DesktopConnectionInfo(
                vnc_connection_info=VNCConnectionInfo(
                    password_authentication_info=VNCPasswordAuthentication(
                        read_write_password="read_write_password_example",
                        read_only_password="read_only_password_example",
                    ),
                ),
            ),
        ),
        status=DesktopResourceStatus(
            gateway_uri="https://desktops.cloud.egov.city/remoteDesktopGateway/",
            stats=DesktopResourceStats(),
        ),
    ) # DesktopResource |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a DesktopResource.
        api_response = api_instance.replace_desktop_resource(resource_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_desktop_resource: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a DesktopResource.
        api_response = api_instance.replace_desktop_resource(resource_id, desktop_resource=desktop_resource)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_desktop_resource: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**| The id of the resource to access |
 **desktop_resource** | [**DesktopResource**](DesktopResource.md)|  | [optional]

### Return type

[**DesktopResource**](DesktopResource.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The DesktopResource was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | DesktopResource does not exist. |  -  |
**409** | The provided DesktopResource conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_file_share_service**
> FileShareService replace_file_share_service(file_share_service_id)

Create or update an FileShareService.

Create or update an FileShareService.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.file_share_service import FileShareService
from agilicus_api.model.error_message import ErrorMessage
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    file_share_service_id = "G" # str | FileShareService unique identifier
    file_share_service = FileShareService(
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
    ) # FileShareService |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update an FileShareService.
        api_response = api_instance.replace_file_share_service(file_share_service_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_file_share_service: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update an FileShareService.
        api_response = api_instance.replace_file_share_service(file_share_service_id, file_share_service=file_share_service)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_file_share_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_share_service_id** | **str**| FileShareService unique identifier |
 **file_share_service** | [**FileShareService**](FileShareService.md)|  | [optional]

### Return type

[**FileShareService**](FileShareService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The FileShareService was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | FileShareService does not exist. |  -  |
**409** | The provided FileShareService conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_service_forwarder**
> ServiceForwarder replace_service_forwarder(service_forwarder_id)

Create or update an ServiceForwarder.

Create or update an ServiceForwarder.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import application_services_api
from agilicus_api.model.service_forwarder import ServiceForwarder
from agilicus_api.model.error_message import ErrorMessage
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
    api_instance = application_services_api.ApplicationServicesApi(api_client)
    service_forwarder_id = "G" # str | Service Forwarder unique identifier
    service_forwarder = ServiceForwarder(
        metadata=MetadataWithId(),
        spec=ServiceForwarderSpec(
            name="name_example",
            org_id="org_id_example",
            bind_address="localhost",
            port=1,
            protocol="tcp",
            application_service_id="application_service_id_example",
            connector_id="123",
        ),
        status=ServiceForwarderStatus(
            connection_uri="connection_uri_example",
            application_service=ApplicationService(
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
            stats=ServiceForwarderStats(),
        ),
    ) # ServiceForwarder |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update an ServiceForwarder.
        api_response = api_instance.replace_service_forwarder(service_forwarder_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_service_forwarder: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update an ServiceForwarder.
        api_response = api_instance.replace_service_forwarder(service_forwarder_id, service_forwarder=service_forwarder)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_service_forwarder: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_forwarder_id** | **str**| Service Forwarder unique identifier |
 **service_forwarder** | [**ServiceForwarder**](ServiceForwarder.md)|  | [optional]

### Return type

[**ServiceForwarder**](ServiceForwarder.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ServiceForwarder was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | ServiceForwarder does not exist. |  -  |
**409** | The provided ServiceForwarder  conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

