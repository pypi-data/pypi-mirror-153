# agilicus_api.MessagesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_message**](MessagesApi.md#create_message) | **POST** /v1/messages/{message_endpoint_id}/send | Send a message to a specific message endpoint.
[**create_user_message**](MessagesApi.md#create_user_message) | **POST** /v1/messages/user/{user_id}/send | Send a message to a user on all (optionally of a type) endpoints.
[**delete_message_endpoint**](MessagesApi.md#delete_message_endpoint) | **DELETE** /v1/messages/{message_endpoint_id} | Delete a messaging endpoint
[**get_message_endpoint**](MessagesApi.md#get_message_endpoint) | **GET** /v1/messages/{message_endpoint_id} | Get a message endpoint
[**list_message_endpoints**](MessagesApi.md#list_message_endpoints) | **GET** /v1/messages | List all message endpoints (all users or a single user)
[**list_messages_config**](MessagesApi.md#list_messages_config) | **GET** /v1/messages/config | Get the config of the endpoint-types (e.g. public keys etc).
[**replace_message_endpoint**](MessagesApi.md#replace_message_endpoint) | **PUT** /v1/messages/{message_endpoint_id} | Update a messaging endpoint
[**update_message_endpoint**](MessagesApi.md#update_message_endpoint) | **POST** /v1/messages/register/{user_id} | Register a messaging endpoint on a user.


# **create_message**
> Message create_message(message_endpoint_id, message)

Send a message to a specific message endpoint.

Send a message to a specific message endpoint.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import messages_api
from agilicus_api.model.message import Message
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
    api_instance = messages_api.MessagesApi(api_client)
    message_endpoint_id = "1234" # str | send a message on a message endpoint
    message = Message(
        title="title_example",
        sub_header="sub_header_example",
        icon="icon_example",
        image="image_example",
        text="text_example",
        uri="uri_example",
        context="context_example",
        actions=[
            MessageAction(
                title="title_example",
                uri="uri_example",
                icon="icon_example",
            ),
        ],
    ) # Message | Message

    # example passing only required values which don't have defaults set
    try:
        # Send a message to a specific message endpoint.
        api_response = api_instance.create_message(message_endpoint_id, message)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->create_message: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_endpoint_id** | **str**| send a message on a message endpoint |
 **message** | [**Message**](Message.md)| Message |

### Return type

[**Message**](Message.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Return the message with uuid filled in |  -  |
**404** | User not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_message**
> Message create_user_message(user_id, message)

Send a message to a user on all (optionally of a type) endpoints.

Send a message to a user on all (optionally of a type) endpoints.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import messages_api
from agilicus_api.model.message import Message
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.message_endpoint_type import MessageEndpointType
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
    api_instance = messages_api.MessagesApi(api_client)
    user_id = "1234" # str | user_id path
    message = Message(
        title="title_example",
        sub_header="sub_header_example",
        icon="icon_example",
        image="image_example",
        text="text_example",
        uri="uri_example",
        context="context_example",
        actions=[
            MessageAction(
                title="title_example",
                uri="uri_example",
                icon="icon_example",
            ),
        ],
    ) # Message | Message
    message_endpoint_type = MessageEndpointType("sms") # MessageEndpointType | messaging endpoint type (optional)
    address = "15555555555" # str | messaging address (direct) (optional)

    # example passing only required values which don't have defaults set
    try:
        # Send a message to a user on all (optionally of a type) endpoints.
        api_response = api_instance.create_user_message(user_id, message)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->create_user_message: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Send a message to a user on all (optionally of a type) endpoints.
        api_response = api_instance.create_user_message(user_id, message, message_endpoint_type=message_endpoint_type, address=address)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->create_user_message: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **message** | [**Message**](Message.md)| Message |
 **message_endpoint_type** | **MessageEndpointType**| messaging endpoint type | [optional]
 **address** | **str**| messaging address (direct) | [optional]

### Return type

[**Message**](Message.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Return the message with uuid filled in |  -  |
**404** | User not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_message_endpoint**
> delete_message_endpoint(message_endpoint_id)

Delete a messaging endpoint

Delete a messaging endpoint

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import messages_api
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
    api_instance = messages_api.MessagesApi(api_client)
    message_endpoint_id = "1234" # str | messaging endpoint id
    user_id = "1234" # str | Query based on user id (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a messaging endpoint
        api_instance.delete_message_endpoint(message_endpoint_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->delete_message_endpoint: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a messaging endpoint
        api_instance.delete_message_endpoint(message_endpoint_id, user_id=user_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->delete_message_endpoint: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_endpoint_id** | **str**| messaging endpoint id |
 **user_id** | **str**| Query based on user id | [optional]

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
**204** | Messaging endpoint deleted |  -  |
**404** | Messaging endpoint not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_message_endpoint**
> MessageEndpoint get_message_endpoint(message_endpoint_id)

Get a message endpoint

Get a message endpoint

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import messages_api
from agilicus_api.model.message_endpoint import MessageEndpoint
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
    api_instance = messages_api.MessagesApi(api_client)
    message_endpoint_id = "1234" # str | messaging endpoint id
    user_id = "1234" # str | Query based on user id (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a message endpoint
        api_response = api_instance.get_message_endpoint(message_endpoint_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->get_message_endpoint: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a message endpoint
        api_response = api_instance.get_message_endpoint(message_endpoint_id, user_id=user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->get_message_endpoint: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_endpoint_id** | **str**| messaging endpoint id |
 **user_id** | **str**| Query based on user id | [optional]

### Return type

[**MessageEndpoint**](MessageEndpoint.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the detail of the message endpoint |  -  |
**404** | Messaging endpoint not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_message_endpoints**
> ListMessageEndpointsResponse list_message_endpoints()

List all message endpoints (all users or a single user)

List all message endpoints (all users or a single user)

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import messages_api
from agilicus_api.model.list_message_endpoints_response import ListMessageEndpointsResponse
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
    api_instance = messages_api.MessagesApi(api_client)
    user_id = "1234" # str | Query based on user id (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List all message endpoints (all users or a single user)
        api_response = api_instance.list_message_endpoints(user_id=user_id, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->list_message_endpoints: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| Query based on user id | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListMessageEndpointsResponse**](ListMessageEndpointsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all message endpoints (for all users if user_id not present) |  -  |
**404** | No messaging endpoints exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_messages_config**
> MessageEndpointsConfig list_messages_config()

Get the config of the endpoint-types (e.g. public keys etc).

Get the config of the endpoint-types (e.g. public keys etc).

### Example

```python
import time
import agilicus_api
from agilicus_api.api import messages_api
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.message_endpoints_config import MessageEndpointsConfig
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)


# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = messages_api.MessagesApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get the config of the endpoint-types (e.g. public keys etc).
        api_response = api_instance.list_messages_config()
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->list_messages_config: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**MessageEndpointsConfig**](MessageEndpointsConfig.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the configuration of the messaging types (e.g. public keys etc). |  -  |
**404** | No messaging endpoints registered. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_message_endpoint**
> MessageEndpoint replace_message_endpoint(message_endpoint_id, message_endpoint)

Update a messaging endpoint

Update a messaging endpoint

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import messages_api
from agilicus_api.model.message_endpoint import MessageEndpoint
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
    api_instance = messages_api.MessagesApi(api_client)
    message_endpoint_id = "1234" # str | messaging endpoint id
    message_endpoint = MessageEndpoint(
        metadata=MessageEndpointMetadata(
        ),
        spec=MessageEndpointSpec(
            endpoint_type=MessageEndpointType("web_push"),
            nickname="nickname_example",
            address="address_example",
            enabled=True,
        ),
    ) # MessageEndpoint | Message
    user_id = "1234" # str | Query based on user id (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a messaging endpoint
        api_response = api_instance.replace_message_endpoint(message_endpoint_id, message_endpoint)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->replace_message_endpoint: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a messaging endpoint
        api_response = api_instance.replace_message_endpoint(message_endpoint_id, message_endpoint, user_id=user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->replace_message_endpoint: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_endpoint_id** | **str**| messaging endpoint id |
 **message_endpoint** | [**MessageEndpoint**](MessageEndpoint.md)| Message |
 **user_id** | **str**| Query based on user id | [optional]

### Return type

[**MessageEndpoint**](MessageEndpoint.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully updated messaging endpoint |  -  |
**404** | Messaging endpoint not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_message_endpoint**
> MessageEndpoint update_message_endpoint(user_id, message_endpoint)

Register a messaging endpoint on a user.

Register a messaging endpoint on a user.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import messages_api
from agilicus_api.model.message_endpoint import MessageEndpoint
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
    api_instance = messages_api.MessagesApi(api_client)
    user_id = "1234" # str | user_id path
    message_endpoint = MessageEndpoint(
        metadata=MessageEndpointMetadata(
        ),
        spec=MessageEndpointSpec(
            endpoint_type=MessageEndpointType("web_push"),
            nickname="nickname_example",
            address="address_example",
            enabled=True,
        ),
    ) # MessageEndpoint | Message

    # example passing only required values which don't have defaults set
    try:
        # Register a messaging endpoint on a user.
        api_response = api_instance.update_message_endpoint(user_id, message_endpoint)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling MessagesApi->update_message_endpoint: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **message_endpoint** | [**MessageEndpoint**](MessageEndpoint.md)| Message |

### Return type

[**MessageEndpoint**](MessageEndpoint.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created messaging endpoint |  -  |
**409** | Duplicate address for this user |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

