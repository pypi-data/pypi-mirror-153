# agilicus_api.ConnectorsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_agent_connector**](ConnectorsApi.md#create_agent_connector) | **POST** /v1/agent_connectors | Create an agent connector
[**create_agent_csr**](ConnectorsApi.md#create_agent_csr) | **POST** /v1/agent_connectors/{connector_id}/certificate_signing_requests | Creates a CertSigningReq
[**create_agent_stats**](ConnectorsApi.md#create_agent_stats) | **POST** /v1/agent_connectors/{connector_id}/stats | Creates an AgentConnectorStats record.
[**create_csr**](ConnectorsApi.md#create_csr) | **POST** /v1/certificate_signing_requests | Creates a CertSigningReq
[**create_ipsec_connector**](ConnectorsApi.md#create_ipsec_connector) | **POST** /v1/ipsec_connectors | Create an IPsec connector
[**delete_agent_connector**](ConnectorsApi.md#delete_agent_connector) | **DELETE** /v1/agent_connectors/{connector_id} | Delete a agent
[**delete_connector**](ConnectorsApi.md#delete_connector) | **DELETE** /v1/connectors/{connector_id} | Delete a connector
[**delete_ipsec_connector**](ConnectorsApi.md#delete_ipsec_connector) | **DELETE** /v1/ipsec_connectors/{connector_id} | Delete an IPsec connector
[**get_agent_connector**](ConnectorsApi.md#get_agent_connector) | **GET** /v1/agent_connectors/{connector_id} | Get an agent
[**get_agent_csr**](ConnectorsApi.md#get_agent_csr) | **GET** /v1/agent_connectors/{connector_id}/certificate_signing_requests/{csr_id} | Update a CertSigningReq
[**get_agent_info**](ConnectorsApi.md#get_agent_info) | **GET** /v1/agent_connectors/{connector_id}/info | Get information associated with connector
[**get_agent_stats**](ConnectorsApi.md#get_agent_stats) | **GET** /v1/agent_connectors/{connector_id}/stats | Get the AgentConnector stats
[**get_connector**](ConnectorsApi.md#get_connector) | **GET** /v1/connectors/{connector_id} | Get a connector
[**get_ipsec_connector**](ConnectorsApi.md#get_ipsec_connector) | **GET** /v1/ipsec_connectors/{connector_id} | Get an IPsec connector
[**get_ipsec_connector_info**](ConnectorsApi.md#get_ipsec_connector_info) | **GET** /v1/ipsec_connectors/{connector_id}/info | Get IPsec connector runtime information
[**list_agent_connector**](ConnectorsApi.md#list_agent_connector) | **GET** /v1/agent_connectors | list agent connectors
[**list_agent_csr**](ConnectorsApi.md#list_agent_csr) | **GET** /v1/agent_connectors/{connector_id}/certificate_signing_requests | list agent connector certificate signing requests
[**list_connector**](ConnectorsApi.md#list_connector) | **GET** /v1/connectors | List connectors
[**list_connector_guid_mapping**](ConnectorsApi.md#list_connector_guid_mapping) | **GET** /v1/connectors/guids | Get all connector guids and a unique name mapping
[**list_ipsec_connector**](ConnectorsApi.md#list_ipsec_connector) | **GET** /v1/ipsec_connectors | list IPsec connectors
[**replace_agent_connector**](ConnectorsApi.md#replace_agent_connector) | **PUT** /v1/agent_connectors/{connector_id} | Update an agent
[**replace_agent_connector_local_auth_info**](ConnectorsApi.md#replace_agent_connector_local_auth_info) | **PUT** /v1/agent_connectors/{connector_id}/local_auth_info | Update an agent&#39;s local authentication information
[**replace_agent_csr**](ConnectorsApi.md#replace_agent_csr) | **PUT** /v1/agent_connectors/{connector_id}/certificate_signing_requests/{csr_id} | Update a CertSigningReq
[**replace_ipsec_connector**](ConnectorsApi.md#replace_ipsec_connector) | **PUT** /v1/ipsec_connectors/{connector_id} | Update an IPsec connector


# **create_agent_connector**
> AgentConnector create_agent_connector(agent_connector)

Create an agent connector

Create an agent connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.agent_connector import AgentConnector
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    agent_connector = AgentConnector(
        metadata=MetadataWithId(),
        spec=AgentConnectorSpec(
            name="name_example",
            name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
            org_id="123",
            max_number_connections=0,
            connection_uri="connection_uri_example",
            service_account_required=True,
            local_authentication_enabled=False,
            provisioning=AgentConnectorSpecProvisioning(
                all_resources=False,
            ),
            routing=AgentConnectorRouting(
                local_binds=[
                    AgentConnectorLocalBind(
                        bind_host="192.168.5.124",
                        bind_port=8443,
                    ),
                ],
            ),
        ),
    ) # AgentConnector | 

    # example passing only required values which don't have defaults set
    try:
        # Create an agent connector
        api_response = api_instance.create_agent_connector(agent_connector)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->create_agent_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_connector** | [**AgentConnector**](AgentConnector.md)|  |

### Return type

[**AgentConnector**](AgentConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New agent |  -  |
**400** | The contents of the request body are invalid |  -  |
**409** | agent already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_agent_csr**
> CertSigningReq create_agent_csr(connector_id, cert_signing_req)

Creates a CertSigningReq

Creates a CertSigningReq 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.cert_signing_req import CertSigningReq
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    cert_signing_req = CertSigningReq(
        metadata=MetadataWithId(),
        spec=CertSigningReqSpec(
            org_id="123",
            auto_renew=True,
            rotate_keys=True,
            private_key_id="private_key_id_example",
            request="request_example",
            target_issuer="agilicus-private",
        ),
        status=CertSigningReqStatus(
            certificates=[
                X509Certificate(
                    metadata=MetadataWithId(),
                    spec=X509CertificateSpec(
                        certificate="certificate_example",
                        csr_id="csr_id_example",
                        org_id="123",
                        message="message_example",
                        reason=CSRReasonEnum("pending"),
                    ),
                    status=X509CertificateStatus(
                    ),
                ),
            ],
        ),
    ) # CertSigningReq | 
    private_key_id = "1234" # str | query by private key id (optional)
    target_issuer = [
        "agilicus-private",
    ] # [str] | A list of target issuers to search for. If an item matches an entry in the list, is returned.  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Creates a CertSigningReq
        api_response = api_instance.create_agent_csr(connector_id, cert_signing_req)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->create_agent_csr: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Creates a CertSigningReq
        api_response = api_instance.create_agent_csr(connector_id, cert_signing_req, private_key_id=private_key_id, target_issuer=target_issuer)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->create_agent_csr: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **cert_signing_req** | [**CertSigningReq**](CertSigningReq.md)|  |
 **private_key_id** | **str**| query by private key id | [optional]
 **target_issuer** | **[str]**| A list of target issuers to search for. If an item matches an entry in the list, is returned.  | [optional]

### Return type

[**CertSigningReq**](CertSigningReq.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | CertSigningReq created and returned. |  -  |
**404** | CertSigningReq does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_agent_stats**
> AgentConnectorStats create_agent_stats(connector_id, agent_connector_stats)

Creates an AgentConnectorStats record.

Publishes the most recent stats collected by the AgentConnector. Currently only the most recent AgentCollectorStats is retained, but in the future some history may be recorded. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.agent_connector_stats import AgentConnectorStats
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    agent_connector_stats = AgentConnectorStats() # AgentConnectorStats | 

    # example passing only required values which don't have defaults set
    try:
        # Creates an AgentConnectorStats record.
        api_response = api_instance.create_agent_stats(connector_id, agent_connector_stats)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->create_agent_stats: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **agent_connector_stats** | [**AgentConnectorStats**](AgentConnectorStats.md)|  |

### Return type

[**AgentConnectorStats**](AgentConnectorStats.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | AgentConnectorStats created and returned. |  -  |
**404** | AgentConnector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_csr**
> CertSigningReq create_csr(cert_signing_req)

Creates a CertSigningReq

Creates a CertSigningReq 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.cert_signing_req import CertSigningReq
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    cert_signing_req = CertSigningReq(
        metadata=MetadataWithId(),
        spec=CertSigningReqSpec(
            org_id="123",
            auto_renew=True,
            rotate_keys=True,
            private_key_id="private_key_id_example",
            request="request_example",
            target_issuer="agilicus-private",
        ),
        status=CertSigningReqStatus(
            certificates=[
                X509Certificate(
                    metadata=MetadataWithId(),
                    spec=X509CertificateSpec(
                        certificate="certificate_example",
                        csr_id="csr_id_example",
                        org_id="123",
                        message="message_example",
                        reason=CSRReasonEnum("pending"),
                    ),
                    status=X509CertificateStatus(
                    ),
                ),
            ],
        ),
    ) # CertSigningReq | 

    # example passing only required values which don't have defaults set
    try:
        # Creates a CertSigningReq
        api_response = api_instance.create_csr(cert_signing_req)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->create_csr: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cert_signing_req** | [**CertSigningReq**](CertSigningReq.md)|  |

### Return type

[**CertSigningReq**](CertSigningReq.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | CertSigningReq created and returned. |  -  |
**404** | CertSigningReq does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_ipsec_connector**
> IpsecConnector create_ipsec_connector(ipsec_connector)

Create an IPsec connector

Create an IPsec connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.ipsec_connector import IpsecConnector
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    ipsec_connector = IpsecConnector(
        metadata=MetadataWithId(),
        spec=IpsecConnectorSpec(
            name="ipsec1",
            name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
            org_id="123",
            ipsec_gateway_id="1234",
            connections=[
                IpsecConnection(
                    name="name_example",
                    inherit_from="inherit_from_example",
                    gateway_interface=IpsecGatewayInterface(
                        name="CWzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyvKX7HzKpul80FcVjSkp5IHYCm6w-v0dZfU7",
                        certificate_dn="C=US, O=LetsEncrypt, CN=R3",
                    ),
                    spec=IpsecConnectionSpec(
                        ike_version="ikev1",
                        remote_ipv4_address="remote_ipv4_address_example",
                        remote_dns_ipv4_address="remote_dns_ipv4_address_example",
                        remote_healthcheck_ipv4_address="remote_healthcheck_ipv4_address_example",
                        ike_cipher_encryption_algorithm=CipherEncryptionAlgorithm("aes128"),
                        ike_cipher_integrity_algorithm=CipherIntegrityAlgorithm("sha256"),
                        ike_cipher_diffie_hellman_group=CipherDiffieHellmanGroup("ecp256"),
                        esp_cipher_encryption_algorithm=CipherEncryptionAlgorithm("aes128"),
                        esp_cipher_integrity_algorithm=CipherIntegrityAlgorithm("sha256"),
                        esp_cipher_diffie_hellman_group=CipherDiffieHellmanGroup("ecp256"),
                        esp_lifetime=1,
                        ike_lifetime=1,
                        ike_rekey=True,
                        ike_reauth=True,
                        ike_authentication_type="ike_preshared_key",
                        ike_preshared_key="ike_preshared_key_example",
                        ike_chain_of_trust_certificates="ike_chain_of_trust_certificates_example",
                        ike_certificate_dn="ike_certificate_dn_example",
                        ike_remote_identity="vpn.my-org.example.com",
                        local_ipv4_block="192.168.3.0/30",
                        remote_ipv4_ranges=[
                            IpsecConnectionIpv4Block(
                                ipv4_address_block="192.168.2.1/30",
                            ),
                        ],
                        use_cert_hash=True,
                        local_certificate_uribase="http://certificates.ca-1.agilicus.ca/certificates/",
                        remote_certificate_uribase="http://certificates.ca-1.agilicus.ca/certificates/",
                    ),
                ),
            ],
        ),
    ) # IpsecConnector | 

    # example passing only required values which don't have defaults set
    try:
        # Create an IPsec connector
        api_response = api_instance.create_ipsec_connector(ipsec_connector)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->create_ipsec_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ipsec_connector** | [**IpsecConnector**](IpsecConnector.md)|  |

### Return type

[**IpsecConnector**](IpsecConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New IPsec connector |  -  |
**400** | The contents of the request body are invalid |  -  |
**409** | IPsec connector already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_agent_connector**
> delete_agent_connector(connector_id)

Delete a agent

Delete a agent

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a agent
        api_instance.delete_agent_connector(connector_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->delete_agent_connector: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a agent
        api_instance.delete_agent_connector(connector_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->delete_agent_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
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
**204** | agent was deleted |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_connector**
> delete_connector(connector_id)

Delete a connector

Delete a connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a connector
        api_instance.delete_connector(connector_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->delete_connector: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a connector
        api_instance.delete_connector(connector_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->delete_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
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
**204** | connector was deleted |  -  |
**404** | connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_ipsec_connector**
> delete_ipsec_connector(connector_id)

Delete an IPsec connector

Delete an IPsec connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete an IPsec connector
        api_instance.delete_ipsec_connector(connector_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->delete_ipsec_connector: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete an IPsec connector
        api_instance.delete_ipsec_connector(connector_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->delete_ipsec_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
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
**204** | IPsec connector was deleted |  -  |
**404** | IPsec connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent_connector**
> AgentConnector get_agent_connector(connector_id)

Get an agent

Get an agent

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.agent_connector import AgentConnector
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get an agent
        api_response = api_instance.get_agent_connector(connector_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_connector: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get an agent
        api_response = api_instance.get_agent_connector(connector_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**AgentConnector**](AgentConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent found and returned |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent_csr**
> CertSigningReq get_agent_csr(connector_id, csr_id)

Update a CertSigningReq

Update a CertSigningReq

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.cert_signing_req import CertSigningReq
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    csr_id = "1234" # str | A certificate signing request id
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a CertSigningReq
        api_response = api_instance.get_agent_csr(connector_id, csr_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_csr: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a CertSigningReq
        api_response = api_instance.get_agent_csr(connector_id, csr_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_csr: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **csr_id** | **str**| A certificate signing request id |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**CertSigningReq**](CertSigningReq.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | CertSigningReq found and returned |  -  |
**404** | CertSigningReq csr does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent_info**
> AgentConnectorInfo get_agent_info(connector_id)

Get information associated with connector

Get information associated with connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.agent_connector_info import AgentConnectorInfo
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)
    allow_list = True # bool | Perform a query that returns the allow list in the response.  (optional)
    service_forwarders = True # bool | Perform a query that returns the service forwarders in the response.  (optional)
    authz_public_key = True # bool | Perform a query that returns the authz public key  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get information associated with connector
        api_response = api_instance.get_agent_info(connector_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_info: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get information associated with connector
        api_response = api_instance.get_agent_info(connector_id, org_id=org_id, allow_list=allow_list, service_forwarders=service_forwarders, authz_public_key=authz_public_key)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_info: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **allow_list** | **bool**| Perform a query that returns the allow list in the response.  | [optional]
 **service_forwarders** | **bool**| Perform a query that returns the service forwarders in the response.  | [optional]
 **authz_public_key** | **bool**| Perform a query that returns the authz public key  | [optional]

### Return type

[**AgentConnectorInfo**](AgentConnectorInfo.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent info found and returned |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent_stats**
> AgentConnectorStats get_agent_stats(connector_id)

Get the AgentConnector stats

Gets the most recent stats published by the AgentConnector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.agent_connector_stats import AgentConnectorStats
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get the AgentConnector stats
        api_response = api_instance.get_agent_stats(connector_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_stats: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get the AgentConnector stats
        api_response = api_instance.get_agent_stats(connector_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_stats: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**AgentConnectorStats**](AgentConnectorStats.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent stats found and returned |  -  |
**404** | AgentConnector does not exist, or has not recently published any stats. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connector**
> Connector get_connector(connector_id)

Get a connector

Get a connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.connector import Connector
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a connector
        api_response = api_instance.get_connector(connector_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_connector: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a connector
        api_response = api_instance.get_connector(connector_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**Connector**](Connector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | connector found and returned |  -  |
**404** | Connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ipsec_connector**
> IpsecConnector get_ipsec_connector(connector_id)

Get an IPsec connector

Get an IPsec connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.ipsec_connector import IpsecConnector
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get an IPsec connector
        api_response = api_instance.get_ipsec_connector(connector_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_ipsec_connector: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get an IPsec connector
        api_response = api_instance.get_ipsec_connector(connector_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_ipsec_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**IpsecConnector**](IpsecConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | IPsec connector found and returned |  -  |
**404** | IPsec connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ipsec_connector_info**
> IpsecConnector get_ipsec_connector_info(connector_id)

Get IPsec connector runtime information

Get IPsec connector runtime information. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.ipsec_connector import IpsecConnector
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get IPsec connector runtime information
        api_response = api_instance.get_ipsec_connector_info(connector_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_ipsec_connector_info: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get IPsec connector runtime information
        api_response = api_instance.get_ipsec_connector_info(connector_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->get_ipsec_connector_info: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**IpsecConnector**](IpsecConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | IPsec connector found and returned |  -  |
**404** | IPsec connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_agent_connector**
> ListAgentConnectorResponse list_agent_connector()

list agent connectors

list agent connectors. By default, an AgentConnector will not show stats when listed to speed up the query. Setting the show_stats parameter to true retrieve the stats for every AgentConnector. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.list_agent_connector_response import ListAgentConnectorResponse
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_id = "1234" # str | Organisation Unique identifier (optional)
    name = "host1_connector" # str | Query the connector by name (optional)
    show_stats = True # bool | Whether the return value should include the stats for included objects. If false the query may run faster but will not include statistics. If not present, defaults to false.  (optional) if omitted the server will use the default value of False
    page_at_id = "foo@example.com" # str | Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_id` field from the list response.  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # list agent connectors
        api_response = api_instance.list_agent_connector(limit=limit, org_id=org_id, name=name, show_stats=show_stats, page_at_id=page_at_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->list_agent_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **name** | **str**| Query the connector by name | [optional]
 **show_stats** | **bool**| Whether the return value should include the stats for included objects. If false the query may run faster but will not include statistics. If not present, defaults to false.  | [optional] if omitted the server will use the default value of False
 **page_at_id** | **str**| Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the &#x60;page_at_id&#x60; field from the list response.  | [optional]

### Return type

[**ListAgentConnectorResponse**](ListAgentConnectorResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of agent connectors |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_agent_csr**
> ListCertSigningReqResponse list_agent_csr(connector_id)

list agent connector certificate signing requests

List agent connector certificate signing requests. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.list_cert_signing_req_response import ListCertSigningReqResponse
from agilicus_api.model.csr_reason_enum import CSRReasonEnum
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    private_key_id = "1234" # str | query by private key id (optional)
    target_issuer = [
        "agilicus-private",
    ] # [str] | A list of target issuers to search for. If an item matches an entry in the list, is returned.  (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_id = "1234" # str | Organisation Unique identifier (optional)
    reason = CSRReasonEnum("pending") # CSRReasonEnum | Query a CSR based on its reason status (optional)
    not_valid_after = "in 30 days" # str | Search criteria for finding expired certificates * In UTC. * Supports human-friendly values. * Example, find all expired certificates in 30 days: not_after_after=\"in 30 days\" * Example, find all expired certificates today:  not_valid_after=\"tomorrow\" * Example, find all expired now:  not_valid_after=\"now\"  (optional)

    # example passing only required values which don't have defaults set
    try:
        # list agent connector certificate signing requests
        api_response = api_instance.list_agent_csr(connector_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->list_agent_csr: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # list agent connector certificate signing requests
        api_response = api_instance.list_agent_csr(connector_id, private_key_id=private_key_id, target_issuer=target_issuer, limit=limit, org_id=org_id, reason=reason, not_valid_after=not_valid_after)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->list_agent_csr: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **private_key_id** | **str**| query by private key id | [optional]
 **target_issuer** | **[str]**| A list of target issuers to search for. If an item matches an entry in the list, is returned.  | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **reason** | **CSRReasonEnum**| Query a CSR based on its reason status | [optional]
 **not_valid_after** | **str**| Search criteria for finding expired certificates * In UTC. * Supports human-friendly values. * Example, find all expired certificates in 30 days: not_after_after&#x3D;\&quot;in 30 days\&quot; * Example, find all expired certificates today:  not_valid_after&#x3D;\&quot;tomorrow\&quot; * Example, find all expired now:  not_valid_after&#x3D;\&quot;now\&quot;  | [optional]

### Return type

[**ListCertSigningReqResponse**](ListCertSigningReqResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of CertSigningReq |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connector**
> ListConnectorResponse list_connector()

List connectors

List connectors. By default, Connectors will not show stats when listed to speed up the query. Set the show_stats parameter to true to retrieve the stats for every Connector. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.list_connector_response import ListConnectorResponse
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_id = "1234" # str | Organisation Unique identifier (optional)
    name = "host1_connector" # str | Query the connector by name (optional)
    type = "agent" # str | connector type (optional)
    show_stats = True # bool | Whether the return value should include the stats for included objects. If false the query may run faster but will not include statistics. If not present, defaults to false.  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List connectors
        api_response = api_instance.list_connector(limit=limit, org_id=org_id, name=name, type=type, show_stats=show_stats)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->list_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **name** | **str**| Query the connector by name | [optional]
 **type** | **str**| connector type | [optional]
 **show_stats** | **bool**| Whether the return value should include the stats for included objects. If false the query may run faster but will not include statistics. If not present, defaults to false.  | [optional] if omitted the server will use the default value of False

### Return type

[**ListConnectorResponse**](ListConnectorResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of connectors |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connector_guid_mapping**
> ListGuidMetadataResponse list_connector_guid_mapping()

Get all connector guids and a unique name mapping

Get all connector guids and a unique name mapping

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.list_guid_metadata_response import ListGuidMetadataResponse
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    connector_id = "1234" # str | connector id in query (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    previous_guid = "73WakrfVbNJBaAmhQtEeDv" # str | Pagination based query with the guid as the key. To get the initial entries supply an empty string. (optional)
    updated_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | query since updated (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all connector guids and a unique name mapping
        api_response = api_instance.list_connector_guid_mapping(org_id=org_id, connector_id=connector_id, limit=limit, previous_guid=previous_guid, updated_since=updated_since)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->list_connector_guid_mapping: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **connector_id** | **str**| connector id in query | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **previous_guid** | **str**| Pagination based query with the guid as the key. To get the initial entries supply an empty string. | [optional]
 **updated_since** | **datetime**| query since updated | [optional]

### Return type

[**ListGuidMetadataResponse**](ListGuidMetadataResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return GuidToName mapping |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_ipsec_connector**
> ListIpsecConnectorResponse list_ipsec_connector()

list IPsec connectors

list IPsec connectors. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.list_ipsec_connector_response import ListIpsecConnectorResponse
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_id = "1234" # str | Organisation Unique identifier (optional)
    name = "host1_connector" # str | Query the connector by name (optional)
    render_inheritance = False # bool | Returns connections with their spec inherited as per their inherited_from property  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # list IPsec connectors
        api_response = api_instance.list_ipsec_connector(limit=limit, org_id=org_id, name=name, render_inheritance=render_inheritance)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->list_ipsec_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **name** | **str**| Query the connector by name | [optional]
 **render_inheritance** | **bool**| Returns connections with their spec inherited as per their inherited_from property  | [optional] if omitted the server will use the default value of False

### Return type

[**ListIpsecConnectorResponse**](ListIpsecConnectorResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of IPsec connectors |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_agent_connector**
> AgentConnector replace_agent_connector(connector_id)

Update an agent

Update an agent

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.agent_connector import AgentConnector
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)
    agent_connector = AgentConnector(
        metadata=MetadataWithId(),
        spec=AgentConnectorSpec(
            name="name_example",
            name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
            org_id="123",
            max_number_connections=0,
            connection_uri="connection_uri_example",
            service_account_required=True,
            local_authentication_enabled=False,
            provisioning=AgentConnectorSpecProvisioning(
                all_resources=False,
            ),
            routing=AgentConnectorRouting(
                local_binds=[
                    AgentConnectorLocalBind(
                        bind_host="192.168.5.124",
                        bind_port=8443,
                    ),
                ],
            ),
        ),
    ) # AgentConnector |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update an agent
        api_response = api_instance.replace_agent_connector(connector_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->replace_agent_connector: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update an agent
        api_response = api_instance.replace_agent_connector(connector_id, org_id=org_id, agent_connector=agent_connector)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->replace_agent_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **agent_connector** | [**AgentConnector**](AgentConnector.md)|  | [optional]

### Return type

[**AgentConnector**](AgentConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent updated |  -  |
**400** | The contents of the request body are invalid |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_agent_connector_local_auth_info**
> AgentConnector replace_agent_connector_local_auth_info(connector_id)

Update an agent's local authentication information

Update an agent's local authentication information. This is typically modified by the agent itself.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.agent_connector import AgentConnector
from agilicus_api.model.agent_local_auth_info import AgentLocalAuthInfo
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    agent_local_auth_info = AgentLocalAuthInfo(
        org_id="123",
        local_authentication_public_key="-----BEGIN PRIVATE KEY-----\nActualKeyContents\n-----END PRIVATE KEY-----\n",
    ) # AgentLocalAuthInfo |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update an agent's local authentication information
        api_response = api_instance.replace_agent_connector_local_auth_info(connector_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->replace_agent_connector_local_auth_info: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update an agent's local authentication information
        api_response = api_instance.replace_agent_connector_local_auth_info(connector_id, agent_local_auth_info=agent_local_auth_info)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->replace_agent_connector_local_auth_info: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **agent_local_auth_info** | [**AgentLocalAuthInfo**](AgentLocalAuthInfo.md)|  | [optional]

### Return type

[**AgentConnector**](AgentConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent updated |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_agent_csr**
> CertSigningReq replace_agent_csr(connector_id, csr_id)

Update a CertSigningReq

Update a CertSigningReq

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.cert_signing_req import CertSigningReq
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    csr_id = "1234" # str | A certificate signing request id
    org_id = "1234" # str | Organisation Unique identifier (optional)
    cert_signing_req = CertSigningReq(
        metadata=MetadataWithId(),
        spec=CertSigningReqSpec(
            org_id="123",
            auto_renew=True,
            rotate_keys=True,
            private_key_id="private_key_id_example",
            request="request_example",
            target_issuer="agilicus-private",
        ),
        status=CertSigningReqStatus(
            certificates=[
                X509Certificate(
                    metadata=MetadataWithId(),
                    spec=X509CertificateSpec(
                        certificate="certificate_example",
                        csr_id="csr_id_example",
                        org_id="123",
                        message="message_example",
                        reason=CSRReasonEnum("pending"),
                    ),
                    status=X509CertificateStatus(
                    ),
                ),
            ],
        ),
    ) # CertSigningReq |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a CertSigningReq
        api_response = api_instance.replace_agent_csr(connector_id, csr_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->replace_agent_csr: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a CertSigningReq
        api_response = api_instance.replace_agent_csr(connector_id, csr_id, org_id=org_id, cert_signing_req=cert_signing_req)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->replace_agent_csr: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **csr_id** | **str**| A certificate signing request id |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **cert_signing_req** | [**CertSigningReq**](CertSigningReq.md)|  | [optional]

### Return type

[**CertSigningReq**](CertSigningReq.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | CertSigningReq updated |  -  |
**400** | The contents of the request body are invalid |  -  |
**404** | CertSigningReq does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_ipsec_connector**
> IpsecConnector replace_ipsec_connector(connector_id)

Update an IPsec connector

Update an IPsec connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import connectors_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.ipsec_connector import IpsecConnector
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
    api_instance = connectors_api.ConnectorsApi(api_client)
    connector_id = "1234" # str | connector id path
    org_id = "1234" # str | Organisation Unique identifier (optional)
    ipsec_connector = IpsecConnector(
        metadata=MetadataWithId(),
        spec=IpsecConnectorSpec(
            name="ipsec1",
            name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
            org_id="123",
            ipsec_gateway_id="1234",
            connections=[
                IpsecConnection(
                    name="name_example",
                    inherit_from="inherit_from_example",
                    gateway_interface=IpsecGatewayInterface(
                        name="CWzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyvKX7HzKpul80FcVjSkp5IHYCm6w-v0dZfU7",
                        certificate_dn="C=US, O=LetsEncrypt, CN=R3",
                    ),
                    spec=IpsecConnectionSpec(
                        ike_version="ikev1",
                        remote_ipv4_address="remote_ipv4_address_example",
                        remote_dns_ipv4_address="remote_dns_ipv4_address_example",
                        remote_healthcheck_ipv4_address="remote_healthcheck_ipv4_address_example",
                        ike_cipher_encryption_algorithm=CipherEncryptionAlgorithm("aes128"),
                        ike_cipher_integrity_algorithm=CipherIntegrityAlgorithm("sha256"),
                        ike_cipher_diffie_hellman_group=CipherDiffieHellmanGroup("ecp256"),
                        esp_cipher_encryption_algorithm=CipherEncryptionAlgorithm("aes128"),
                        esp_cipher_integrity_algorithm=CipherIntegrityAlgorithm("sha256"),
                        esp_cipher_diffie_hellman_group=CipherDiffieHellmanGroup("ecp256"),
                        esp_lifetime=1,
                        ike_lifetime=1,
                        ike_rekey=True,
                        ike_reauth=True,
                        ike_authentication_type="ike_preshared_key",
                        ike_preshared_key="ike_preshared_key_example",
                        ike_chain_of_trust_certificates="ike_chain_of_trust_certificates_example",
                        ike_certificate_dn="ike_certificate_dn_example",
                        ike_remote_identity="vpn.my-org.example.com",
                        local_ipv4_block="192.168.3.0/30",
                        remote_ipv4_ranges=[
                            IpsecConnectionIpv4Block(
                                ipv4_address_block="192.168.2.1/30",
                            ),
                        ],
                        use_cert_hash=True,
                        local_certificate_uribase="http://certificates.ca-1.agilicus.ca/certificates/",
                        remote_certificate_uribase="http://certificates.ca-1.agilicus.ca/certificates/",
                    ),
                ),
            ],
        ),
    ) # IpsecConnector |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update an IPsec connector
        api_response = api_instance.replace_ipsec_connector(connector_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->replace_ipsec_connector: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update an IPsec connector
        api_response = api_instance.replace_ipsec_connector(connector_id, org_id=org_id, ipsec_connector=ipsec_connector)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ConnectorsApi->replace_ipsec_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **ipsec_connector** | [**IpsecConnector**](IpsecConnector.md)|  | [optional]

### Return type

[**IpsecConnector**](IpsecConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | IPsec connector updated |  -  |
**400** | The contents of the request body are invalid |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

