# agilicus_api.OrganisationsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_billing_portal_link**](OrganisationsApi.md#create_billing_portal_link) | **POST** /v1/orgs/{org_id}/billing_portal_links | Create a link to the billing portal
[**create_blocking_upgrade_orgs_task**](OrganisationsApi.md#create_blocking_upgrade_orgs_task) | **POST** /v1/orgs/upgrade | utility to upgrade organisations
[**create_org**](OrganisationsApi.md#create_org) | **POST** /v1/orgs | Create an organisation
[**create_sub_org**](OrganisationsApi.md#create_sub_org) | **POST** /v1/orgs/{org_id}/orgs | Create a sub organisation
[**delete_sub_org**](OrganisationsApi.md#delete_sub_org) | **DELETE** /v1/orgs/{org_id}/orgs/{sub_org_id} | Delete a sub organisation
[**get_org**](OrganisationsApi.md#get_org) | **GET** /v1/orgs/{org_id} | Get a single organisation
[**get_org_billing_account**](OrganisationsApi.md#get_org_billing_account) | **GET** /v1/orgs/{org_id}/billing_account | Get the billing account associated with the organisation
[**get_org_status**](OrganisationsApi.md#get_org_status) | **GET** /v1/orgs/{org_id}/status | Get the status of an organisation
[**get_usage_metrics**](OrganisationsApi.md#get_usage_metrics) | **GET** /v1/orgs/usage_metrics | Get all usage metrics for an organisation
[**list_email_domains**](OrganisationsApi.md#list_email_domains) | **GET** /v1/orgs/{org_id}/domains | List all unique email domains for users that are inside an organisation
[**list_org_guid_mapping**](OrganisationsApi.md#list_org_guid_mapping) | **GET** /v1/orgs/guids | Get all org guids and a unique name mapping
[**list_orgs**](OrganisationsApi.md#list_orgs) | **GET** /v1/orgs | Get all organisations
[**list_sub_orgs**](OrganisationsApi.md#list_sub_orgs) | **GET** /v1/orgs/{org_id}/orgs | Get all sub organisations
[**replace_org**](OrganisationsApi.md#replace_org) | **PUT** /v1/orgs/{org_id} | Create or update an organisation


# **create_billing_portal_link**
> BillingPortalLink create_billing_portal_link(org_id, billing_portal_link)

Create a link to the billing portal

Creates a temporary, one-time-use link to the billing system's self-serve portal. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.billing_portal_link import BillingPortalLink
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    billing_portal_link = BillingPortalLink(
        return_uri="https://admin.agilicus.cloud/billing?org_id=xyz123",
    ) # BillingPortalLink | 

    # example passing only required values which don't have defaults set
    try:
        # Create a link to the billing portal
        api_response = api_instance.create_billing_portal_link(org_id, billing_portal_link)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->create_billing_portal_link: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **billing_portal_link** | [**BillingPortalLink**](BillingPortalLink.md)|  |

### Return type

[**BillingPortalLink**](BillingPortalLink.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The link was succesfully created. Send the user to the URI provided in the response.  |  -  |
**400** | There was a problem creating the link. Consult the error message for more details.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_blocking_upgrade_orgs_task**
> create_blocking_upgrade_orgs_task()

utility to upgrade organisations

utility to upgrade organisations

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
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
    api_instance = organisations_api.OrganisationsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # utility to upgrade organisations
        api_instance.create_blocking_upgrade_orgs_task()
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->create_blocking_upgrade_orgs_task: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

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
**204** | organisations upgraded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_org**
> Organisation create_org(organisation_admin)

Create an organisation

Create an organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.organisation import Organisation
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.organisation_admin import OrganisationAdmin
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    organisation_admin = OrganisationAdmin(
        issuer="app1",
        organisation="some name",
        subdomain="example.com",
        parent_id="123",
    ) # OrganisationAdmin | 

    # example passing only required values which don't have defaults set
    try:
        # Create an organisation
        api_response = api_instance.create_org(organisation_admin)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->create_org: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organisation_admin** | [**OrganisationAdmin**](OrganisationAdmin.md)|  |

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New organisation created |  -  |
**400** | New organisation created |  -  |
**409** | Organisation already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_sub_org**
> Organisation create_sub_org(org_id, organisation)

Create a sub organisation

Create a sub organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.organisation import Organisation
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    organisation = Organisation(
        all_users_group_id="123",
        all_users_all_suborgs_group_id="123",
        all_users_direct_suborgs_group_id="123",
        auto_created_users_group_id="123",
        external_id="123",
        organisation="some name",
        issuer="app1",
        issuer_id="123",
        subdomain="app1.example.com",
        name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
        contact_id="123",
        parent_id="123",
        root_org_id="aB29sdkD3jlaAbl7",
        auto_create=False,
        trust_on_first_use_duration=86400,
        feature_flags=[
            FeatureFlag(
                feature="saml_auth",
                enabled=True,
                setting="stable",
            ),
        ],
        admin_state=OrganisationStateSelector("active"),
        status=OrganisationStatus(
            all_up=True,
            admin_up=True,
            issuer_up=True,
            current_state=OrganisationStateStatus("active"),
        ),
        billing_account_id="123",
        shard="A",
        cluster="ca-1",
    ) # Organisation | 

    # example passing only required values which don't have defaults set
    try:
        # Create a sub organisation
        api_response = api_instance.create_sub_org(org_id, organisation)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->create_sub_org: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **organisation** | [**Organisation**](Organisation.md)|  |

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New sub organisation created |  -  |
**409** | Organisation already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_sub_org**
> delete_sub_org(org_id, sub_org_id)

Delete a sub organisation

Delete a sub organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    sub_org_id = "1234" # str | Sub Organisation Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Delete a sub organisation
        api_instance.delete_sub_org(org_id, sub_org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->delete_sub_org: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **sub_org_id** | **str**| Sub Organisation Unique identifier |

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
**204** | Organisation was deleted |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_org**
> Organisation get_org(org_id)

Get a single organisation

Get a single organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.organisation import Organisation
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Get a single organisation
        api_response = api_instance.get_org(org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->get_org: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return organisation |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_org_billing_account**
> BillingAccount get_org_billing_account(org_id)

Get the billing account associated with the organisation

Get the billing account associated with the organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.billing_account import BillingAccount
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False
    get_customer_data = False # bool | In billing response, return customer data (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get the billing account associated with the organisation
        api_response = api_instance.get_org_billing_account(org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->get_org_billing_account: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get the billing account associated with the organisation
        api_response = api_instance.get_org_billing_account(org_id, get_subscription_data=get_subscription_data, get_customer_data=get_customer_data)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->get_org_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **get_subscription_data** | **bool**| In billing response, return subscription data | [optional] if omitted the server will use the default value of False
 **get_customer_data** | **bool**| In billing response, return customer data | [optional] if omitted the server will use the default value of False

### Return type

[**BillingAccount**](BillingAccount.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return BillingAccount |  -  |
**404** | Billing account does not exist for this organisation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_org_status**
> OrganisationStatus get_org_status(org_id)

Get the status of an organisation

Get the status of an organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.organisation_status import OrganisationStatus
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Get the status of an organisation
        api_response = api_instance.get_org_status(org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->get_org_status: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |

### Return type

[**OrganisationStatus**](OrganisationStatus.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return organisation status |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usage_metrics**
> UsageMetrics get_usage_metrics(org_id)

Get all usage metrics for an organisation

Get all usage metrics for an organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.usage_metrics import UsageMetrics
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Get all usage metrics for an organisation
        api_response = api_instance.get_usage_metrics(org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->get_usage_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |

### Return type

[**UsageMetrics**](UsageMetrics.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return usage metrics |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_email_domains**
> ListDomainsResponse list_email_domains(org_id)

List all unique email domains for users that are inside an organisation

List all unique email domains for users that are inside an organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.list_domains_response import ListDomainsResponse
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # List all unique email domains for users that are inside an organisation
        api_response = api_instance.list_email_domains(org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->list_email_domains: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |

### Return type

[**ListDomainsResponse**](ListDomainsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of unique email domains inside an organisation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_org_guid_mapping**
> ListGuidMetadataResponse list_org_guid_mapping()

Get all org guids and a unique name mapping

Get all org guids and a unique name mapping

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    previous_guid = "73WakrfVbNJBaAmhQtEeDv" # str | Pagination based query with the guid as the key. To get the initial entries supply an empty string. (optional)
    updated_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | query since updated (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all org guids and a unique name mapping
        api_response = api_instance.list_org_guid_mapping(org_id=org_id, limit=limit, previous_guid=previous_guid, updated_since=updated_since)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->list_org_guid_mapping: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional]
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

# **list_orgs**
> ListOrgsResponse list_orgs()

Get all organisations

Get all organisations

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.list_orgs_response import ListOrgsResponse
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_id = "1234" # str | Organisation Unique identifier (optional)
    organisation = "agilicus" # str | Organisation Name (optional)
    issuer = "example.com" # str | Organisation issuer (optional)
    list_children = False # bool | Controls whether or not children of the matching resources are returned in the listing.  (optional) if omitted the server will use the default value of False
    updated_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | query since updated (optional)
    suborg_updated = True # bool | query any orgs who are updated or have their suborgs updated (optional)
    enabled = True # bool | query any orgs which are enabled (optional)
    billing_account_id = "1234" # str, none_type | Billing account Unique identifier to search for. If `\"\"`, search for something that does not have a billing account.  (optional)
    shard = "A" # str | Hosting shard name (optional)
    cluster = "ca-1" # str | Hosting cluster name (optional)
    subdomain = "agilicus.cloud" # str | query based on organisation subdomain  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all organisations
        api_response = api_instance.list_orgs(limit=limit, org_id=org_id, organisation=organisation, issuer=issuer, list_children=list_children, updated_since=updated_since, suborg_updated=suborg_updated, enabled=enabled, billing_account_id=billing_account_id, shard=shard, cluster=cluster, subdomain=subdomain)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->list_orgs: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **organisation** | **str**| Organisation Name | [optional]
 **issuer** | **str**| Organisation issuer | [optional]
 **list_children** | **bool**| Controls whether or not children of the matching resources are returned in the listing.  | [optional] if omitted the server will use the default value of False
 **updated_since** | **datetime**| query since updated | [optional]
 **suborg_updated** | **bool**| query any orgs who are updated or have their suborgs updated | [optional]
 **enabled** | **bool**| query any orgs which are enabled | [optional]
 **billing_account_id** | **str, none_type**| Billing account Unique identifier to search for. If &#x60;\&quot;\&quot;&#x60;, search for something that does not have a billing account.  | [optional]
 **shard** | **str**| Hosting shard name | [optional]
 **cluster** | **str**| Hosting cluster name | [optional]
 **subdomain** | **str**| query based on organisation subdomain  | [optional]

### Return type

[**ListOrgsResponse**](ListOrgsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return organisations |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_sub_orgs**
> ListOrgsResponse list_sub_orgs(org_id)

Get all sub organisations

Get all sub organisations

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.list_orgs_response import ListOrgsResponse
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    updated_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | query since updated (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all sub organisations
        api_response = api_instance.list_sub_orgs(org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->list_sub_orgs: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all sub organisations
        api_response = api_instance.list_sub_orgs(org_id, limit=limit, updated_since=updated_since)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->list_sub_orgs: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **updated_since** | **datetime**| query since updated | [optional]

### Return type

[**ListOrgsResponse**](ListOrgsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return sub-organisations |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_org**
> replace_org(org_id)

Create or update an organisation

Create or update an organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import organisations_api
from agilicus_api.model.organisation import Organisation
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
    api_instance = organisations_api.OrganisationsApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    organisation = Organisation(
        all_users_group_id="123",
        all_users_all_suborgs_group_id="123",
        all_users_direct_suborgs_group_id="123",
        auto_created_users_group_id="123",
        external_id="123",
        organisation="some name",
        issuer="app1",
        issuer_id="123",
        subdomain="app1.example.com",
        name_slug=K8sSlug("81c2v7s6djuy1zmetozkhdomha1bae37b8ocvx8o53ow2eg7p6qw9qklp6l4y010fogx"),
        contact_id="123",
        parent_id="123",
        root_org_id="aB29sdkD3jlaAbl7",
        auto_create=False,
        trust_on_first_use_duration=86400,
        feature_flags=[
            FeatureFlag(
                feature="saml_auth",
                enabled=True,
                setting="stable",
            ),
        ],
        admin_state=OrganisationStateSelector("active"),
        status=OrganisationStatus(
            all_up=True,
            admin_up=True,
            issuer_up=True,
            current_state=OrganisationStateStatus("active"),
        ),
        billing_account_id="123",
        shard="A",
        cluster="ca-1",
    ) # Organisation |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update an organisation
        api_instance.replace_org(org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->replace_org: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update an organisation
        api_instance.replace_org(org_id, organisation=organisation)
    except agilicus_api.ApiException as e:
        print("Exception when calling OrganisationsApi->replace_org: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **organisation** | [**Organisation**](Organisation.md)|  | [optional]

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Organisation updated |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

