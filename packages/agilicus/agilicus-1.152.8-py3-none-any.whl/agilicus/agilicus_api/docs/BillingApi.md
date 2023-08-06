# agilicus_api.BillingApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_billing_usage_record**](BillingApi.md#add_billing_usage_record) | **POST** /v1/billing_accounts/{billing_account_id}/usage_records | Add usage records for a billing account
[**add_org_to_billing_account**](BillingApi.md#add_org_to_billing_account) | **POST** /v1/billing_accounts/{billing_account_id}/orgs | Add an org to a billing account
[**create_billing_account**](BillingApi.md#create_billing_account) | **POST** /v1/billing_accounts | Create a billing account
[**create_product**](BillingApi.md#create_product) | **POST** /v1/products | Create a product
[**delete_billing_account**](BillingApi.md#delete_billing_account) | **DELETE** /v1/billing_accounts/{billing_account_id} | Delete a billing account
[**delete_product**](BillingApi.md#delete_product) | **DELETE** /v1/products/{product_id} | Delete a product
[**get_billing_account**](BillingApi.md#get_billing_account) | **GET** /v1/billing_accounts/{billing_account_id} | Get a single billing account
[**get_billing_account_orgs**](BillingApi.md#get_billing_account_orgs) | **GET** /v1/billing_accounts/{billing_account_id}/orgs | Get all orgs in a billing account
[**get_product**](BillingApi.md#get_product) | **GET** /v1/products/{product_id} | Get a single product
[**get_usage_records**](BillingApi.md#get_usage_records) | **GET** /v1/billing_accounts/{billing_account_id}/usage_records | Get all subscription usage records
[**list_billing_accounts**](BillingApi.md#list_billing_accounts) | **GET** /v1/billing_accounts | Get all billing accounts
[**list_products**](BillingApi.md#list_products) | **GET** /v1/products | Get all products
[**remove_org_from_billing_account**](BillingApi.md#remove_org_from_billing_account) | **DELETE** /v1/billing_accounts/{billing_account_id}/orgs/{org_id} | Remove an org from a billing account
[**replace_billing_account**](BillingApi.md#replace_billing_account) | **PUT** /v1/billing_accounts/{billing_account_id} | Create or update a billing account
[**replace_product**](BillingApi.md#replace_product) | **PUT** /v1/products/{product_id} | Create or update a product


# **add_billing_usage_record**
> CreateBillingUsageRecords add_billing_usage_record(billing_account_id)

Add usage records for a billing account

Add usage records for a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.create_billing_usage_records import CreateBillingUsageRecords
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
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    create_billing_usage_records = CreateBillingUsageRecords(
        dry_run=False,
        usage_records=[
            BillingUsageRecord(
                dry_run=False,
            ),
        ],
    ) # CreateBillingUsageRecords |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Add usage records for a billing account
        api_response = api_instance.add_billing_usage_record(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_billing_usage_record: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Add usage records for a billing account
        api_response = api_instance.add_billing_usage_record(billing_account_id, create_billing_usage_records=create_billing_usage_records)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_billing_usage_record: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **create_billing_usage_records** | [**CreateBillingUsageRecords**](CreateBillingUsageRecords.md)|  | [optional]

### Return type

[**CreateBillingUsageRecords**](CreateBillingUsageRecords.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Usage records created. |  -  |
**204** | No usage records created. This is due to either no subscriptions found for the customer or no active resources found.  |  -  |
**400** | Error creating usage records |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_org_to_billing_account**
> Organisation add_org_to_billing_account(billing_account_id)

Add an org to a billing account

Add an org to a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.organisation import Organisation
from agilicus_api.model.billing_org import BillingOrg
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
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    billing_org = BillingOrg(
    ) # BillingOrg |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Add an org to a billing account
        api_response = api_instance.add_org_to_billing_account(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_org_to_billing_account: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Add an org to a billing account
        api_response = api_instance.add_org_to_billing_account(billing_account_id, billing_org=billing_org)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->add_org_to_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **billing_org** | [**BillingOrg**](BillingOrg.md)|  | [optional]

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
**200** | Org added to billing account |  -  |
**404** | BillingAccount or Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_billing_account**
> BillingAccount create_billing_account(billing_account)

Create a billing account

Create a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.error_message import ErrorMessage
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
    api_instance = billing_api.BillingApi(api_client)
    billing_account = BillingAccount(
        metadata=MetadataWithId(),
        spec=BillingAccountSpec(
            customer_id="123",
            product_id="123",
            dev_mode=True,
        ),
        status=BillingAccountStatus(
            orgs=[
                Organisation(
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
                ),
            ],
            subscriptions=[
                BillingSubscription(
                    id="id_example",
                ),
            ],
            customer=BillingCustomer(
                name="John Smith",
                email="john@example.com",
            ),
            products=[
                BillingProduct(
                    name="name_example",
                ),
            ],
            product=Product(
                metadata=MetadataWithId(),
                spec=ProductSpec(
                    name="name_example",
                    dev_mode=True,
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                ),
                status=ProductStatus(
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                ),
            ),
        ),
    ) # BillingAccount | 

    # example passing only required values which don't have defaults set
    try:
        # Create a billing account
        api_response = api_instance.create_billing_account(billing_account)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->create_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account** | [**BillingAccount**](BillingAccount.md)|  |

### Return type

[**BillingAccount**](BillingAccount.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New billing account created |  -  |
**400** | Error creating billing account |  -  |
**409** | Billing account already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_product**
> Product create_product(product)

Create a product

Create a product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.product import Product
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
    api_instance = billing_api.BillingApi(api_client)
    product = Product(
        metadata=MetadataWithId(),
        spec=ProductSpec(
            name="name_example",
            dev_mode=True,
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
        ),
        status=ProductStatus(
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
        ),
    ) # Product | 

    # example passing only required values which don't have defaults set
    try:
        # Create a product
        api_response = api_instance.create_product(product)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->create_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product** | [**Product**](Product.md)|  |

### Return type

[**Product**](Product.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New product created |  -  |
**400** | Error creating product |  -  |
**409** | Product already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_billing_account**
> delete_billing_account(billing_account_id)

Delete a billing account

Delete a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
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
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Delete a billing account
        api_instance.delete_billing_account(billing_account_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->delete_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |

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
**204** | Billing account has been deleted |  -  |
**404** | Billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_product**
> delete_product(product_id)

Delete a product

Delete a product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
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
    api_instance = billing_api.BillingApi(api_client)
    product_id = "1234" # str | Product Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Delete a product
        api_instance.delete_product(product_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->delete_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product_id** | **str**| Product Unique identifier |

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
**204** | Product has been deleted |  -  |
**404** | Product does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_billing_account**
> BillingAccount get_billing_account(billing_account_id)

Get a single billing account

Get a single billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
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
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    org_id = "1234" # str | Organisation Unique identifier (optional)
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False
    get_customer_data = False # bool | In billing response, return customer data (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get a single billing account
        api_response = api_instance.get_billing_account(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_billing_account: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single billing account
        api_response = api_instance.get_billing_account(billing_account_id, org_id=org_id, get_subscription_data=get_subscription_data, get_customer_data=get_customer_data)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **org_id** | **str**| Organisation Unique identifier | [optional]
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
**200** | Return billing account |  -  |
**404** | billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_billing_account_orgs**
> ListOrgsResponse get_billing_account_orgs(billing_account_id)

Get all orgs in a billing account

Get all orgs in a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
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
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    try:
        # Get all orgs in a billing account
        api_response = api_instance.get_billing_account_orgs(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_billing_account_orgs: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all orgs in a billing account
        api_response = api_instance.get_billing_account_orgs(billing_account_id, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_billing_account_orgs: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

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
**200** | Return billing account |  -  |
**404** | billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_product**
> Product get_product(product_id)

Get a single product

Get a single product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.product import Product
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
    api_instance = billing_api.BillingApi(api_client)
    product_id = "1234" # str | Product Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Get a single product
        api_response = api_instance.get_product(product_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product_id** | **str**| Product Unique identifier |

### Return type

[**Product**](Product.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a product |  -  |
**404** | product does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usage_records**
> ListBillingUsageRecordsResponse get_usage_records(billing_account_id)

Get all subscription usage records

Get all subscription usage records

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_billing_usage_records_response import ListBillingUsageRecordsResponse
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
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    try:
        # Get all subscription usage records
        api_response = api_instance.get_usage_records(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_usage_records: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all subscription usage records
        api_response = api_instance.get_usage_records(billing_account_id, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->get_usage_records: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListBillingUsageRecordsResponse**](ListBillingUsageRecordsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return all Usage records for the associated billing account |  -  |
**404** | billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_billing_accounts**
> ListBillingAccountsResponse list_billing_accounts()

Get all billing accounts

Get all billing accounts

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_billing_accounts_response import ListBillingAccountsResponse
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
    api_instance = billing_api.BillingApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    org_id = "1234" # str | Organisation Unique identifier (optional)
    customer_id = "1234" # str | query by billing customer id (optional)
    get_subscription_data = False # bool | In billing response, return subscription data (optional) if omitted the server will use the default value of False
    get_customer_data = False # bool | In billing response, return customer data (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all billing accounts
        api_response = api_instance.list_billing_accounts(limit=limit, org_id=org_id, customer_id=customer_id, get_subscription_data=get_subscription_data, get_customer_data=get_customer_data)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_billing_accounts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **customer_id** | **str**| query by billing customer id | [optional]
 **get_subscription_data** | **bool**| In billing response, return subscription data | [optional] if omitted the server will use the default value of False
 **get_customer_data** | **bool**| In billing response, return customer data | [optional] if omitted the server will use the default value of False

### Return type

[**ListBillingAccountsResponse**](ListBillingAccountsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return billing accounts |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_products**
> ListProductsResponse list_products()

Get all products

Get all products

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.list_products_response import ListProductsResponse
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
    api_instance = billing_api.BillingApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all products
        api_response = api_instance.list_products(limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->list_products: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListProductsResponse**](ListProductsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return billing accounts |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_org_from_billing_account**
> remove_org_from_billing_account(billing_account_id, org_id)

Remove an org from a billing account

From an org from a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
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
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    org_id = "1234" # str | Organisation Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Remove an org from a billing account
        api_instance.remove_org_from_billing_account(billing_account_id, org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->remove_org_from_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **org_id** | **str**| Organisation Unique identifier |

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
**204** | Organisation removed from billing account |  -  |
**404** | Billing account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_billing_account**
> BillingAccount replace_billing_account(billing_account_id)

Create or update a billing account

Create or update a billing account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
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
    api_instance = billing_api.BillingApi(api_client)
    billing_account_id = "1234" # str | Billing account Unique identifier
    billing_account = BillingAccount(
        metadata=MetadataWithId(),
        spec=BillingAccountSpec(
            customer_id="123",
            product_id="123",
            dev_mode=True,
        ),
        status=BillingAccountStatus(
            orgs=[
                Organisation(
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
                ),
            ],
            subscriptions=[
                BillingSubscription(
                    id="id_example",
                ),
            ],
            customer=BillingCustomer(
                name="John Smith",
                email="john@example.com",
            ),
            products=[
                BillingProduct(
                    name="name_example",
                ),
            ],
            product=Product(
                metadata=MetadataWithId(),
                spec=ProductSpec(
                    name="name_example",
                    dev_mode=True,
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                ),
                status=ProductStatus(
                    billing_product_prices=[
                        BillingProductPrice(
                            id="id_example",
                        ),
                    ],
                ),
            ),
        ),
    ) # BillingAccount |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a billing account
        api_response = api_instance.replace_billing_account(billing_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_billing_account: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a billing account
        api_response = api_instance.replace_billing_account(billing_account_id, billing_account=billing_account)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_billing_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_id** | **str**| Billing account Unique identifier |
 **billing_account** | [**BillingAccount**](BillingAccount.md)|  | [optional]

### Return type

[**BillingAccount**](BillingAccount.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated billing account |  -  |
**404** | BillingAccount does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_product**
> Product replace_product(product_id)

Create or update a product

Create or update a product

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import billing_api
from agilicus_api.model.product import Product
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
    api_instance = billing_api.BillingApi(api_client)
    product_id = "1234" # str | Product Unique identifier
    product = Product(
        metadata=MetadataWithId(),
        spec=ProductSpec(
            name="name_example",
            dev_mode=True,
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
        ),
        status=ProductStatus(
            billing_product_prices=[
                BillingProductPrice(
                    id="id_example",
                ),
            ],
        ),
    ) # Product |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a product
        api_response = api_instance.replace_product(product_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_product: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a product
        api_response = api_instance.replace_product(product_id, product=product)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling BillingApi->replace_product: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product_id** | **str**| Product Unique identifier |
 **product** | [**Product**](Product.md)|  | [optional]

### Return type

[**Product**](Product.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated product |  -  |
**404** | BillingAccount does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

