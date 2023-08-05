# agilicus_api.UsersApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bulk_update_metadata**](UsersApi.md#bulk_update_metadata) | **POST** /v1/user_metadata_rpc/bulk_update | Update a group of user&#39;s metadata for the specified org
[**create_challenge_method**](UsersApi.md#create_challenge_method) | **POST** /users/{user_id}/mfa_challenge_methods | Create a multi-factor authentication method
[**create_service_account**](UsersApi.md#create_service_account) | **POST** /v1/service_accounts | Create a service account
[**create_upstream_user_identity**](UsersApi.md#create_upstream_user_identity) | **POST** /users/{user_id}/upstream_user_identities | Create an upstream user identity
[**create_user**](UsersApi.md#create_user) | **POST** /users | Create a user
[**create_user_identity_update**](UsersApi.md#create_user_identity_update) | **POST** /users/{user_id}/user_identity_updates | Update a user&#39;s core identity information.
[**create_user_metadata**](UsersApi.md#create_user_metadata) | **POST** /v1/user_metadata | Create a metadata entry for the user
[**create_user_request**](UsersApi.md#create_user_request) | **POST** /v1/user_requests | Create a request on behalf of the user
[**delete_challenge_method**](UsersApi.md#delete_challenge_method) | **DELETE** /users/{user_id}/mfa_challenge_methods/{challenge_method_id} | Delete a user&#39;s multi-factor authentication challenge method
[**delete_service_account**](UsersApi.md#delete_service_account) | **DELETE** /v1/service_accounts/{service_account_id} | Delete a service account
[**delete_upstream_user_identity**](UsersApi.md#delete_upstream_user_identity) | **DELETE** /users/{user_id}/upstream_user_identities/{upstream_user_identity_id} | Delete an upstream user identity
[**delete_user**](UsersApi.md#delete_user) | **DELETE** /v1/orgs/{org_id}/users/{user_id} | Remove a user from an organisation
[**delete_user_metadata**](UsersApi.md#delete_user_metadata) | **DELETE** /v1/user_metadata/{metadata_id} | Delete an user metadata entry
[**delete_user_request**](UsersApi.md#delete_user_request) | **DELETE** /v1/user_requests/{user_request_id} | Delete an user request
[**get_challenge_method**](UsersApi.md#get_challenge_method) | **GET** /users/{user_id}/mfa_challenge_methods/{challenge_method_id} | Get a single challenge method for the given user
[**get_service_account**](UsersApi.md#get_service_account) | **GET** /v1/service_accounts/{service_account_id} | Get a service account
[**get_upstream_user_identity**](UsersApi.md#get_upstream_user_identity) | **GET** /users/{user_id}/upstream_user_identities/{upstream_user_identity_id} | Get a single upstream user identity
[**get_user**](UsersApi.md#get_user) | **GET** /users/{user_id} | Get a single user
[**get_user_metadata**](UsersApi.md#get_user_metadata) | **GET** /v1/user_metadata/{metadata_id} | Get a single user metadata entry
[**get_user_request**](UsersApi.md#get_user_request) | **GET** /v1/user_requests/{user_request_id} | Get a single user request
[**list_access_requests**](UsersApi.md#list_access_requests) | **GET** /v1/access_requests | Get a list of access requests
[**list_all_resource_permissions**](UsersApi.md#list_all_resource_permissions) | **GET** /users/{user_id}/render_resource_permissions | Return all per-resource permissions for a user
[**list_all_user_orgs**](UsersApi.md#list_all_user_orgs) | **GET** /users/{user_id}/orgs | Return all organisations a user has been assigned to
[**list_all_user_roles**](UsersApi.md#list_all_user_roles) | **GET** /users/{user_id}/render_roles | Return all roles for a user
[**list_challenge_methods**](UsersApi.md#list_challenge_methods) | **GET** /users/{user_id}/mfa_challenge_methods | Get all of a user&#39;s multi-factor authentication challenge method configuration
[**list_combined_user_details**](UsersApi.md#list_combined_user_details) | **GET** /v1/combined_user_details | Get all combined details about users
[**list_desktop_access_info**](UsersApi.md#list_desktop_access_info) | **GET** /v1/user_desktop_access_info | Query various users&#39; desktop access information
[**list_org_user_roles**](UsersApi.md#list_org_user_roles) | **GET** /users/org_user_roles | Get all org user roles
[**list_service_accounts**](UsersApi.md#list_service_accounts) | **GET** /v1/service_accounts | List service accounts
[**list_upstream_user_identities**](UsersApi.md#list_upstream_user_identities) | **GET** /users/{user_id}/upstream_user_identities | Get all of a user&#39;s upstream user identities
[**list_user_application_access_info**](UsersApi.md#list_user_application_access_info) | **GET** /v1/user_application_access_info | Query various users&#39; application access information
[**list_user_file_share_access_info**](UsersApi.md#list_user_file_share_access_info) | **GET** /v1/user_file_share_access_info | Query various users&#39; file share access information
[**list_user_guid_mapping**](UsersApi.md#list_user_guid_mapping) | **GET** /users/guids | Get all user guids and a unique name mapping
[**list_user_guids**](UsersApi.md#list_user_guids) | **GET** /users_ids | Get a list of all user GUIDs
[**list_user_launcher_access_info**](UsersApi.md#list_user_launcher_access_info) | **GET** /v1/user_launcher_access_info | Query various users&#39; launchers access information
[**list_user_metadata**](UsersApi.md#list_user_metadata) | **GET** /v1/user_metadata | Get a list of user metadata entries
[**list_user_permissions**](UsersApi.md#list_user_permissions) | **GET** /users/{user_id}/host_permissions | Return the user&#39;s host permissions
[**list_user_requests**](UsersApi.md#list_user_requests) | **GET** /v1/user_requests | Get a list of user requests
[**list_user_resource_access_info**](UsersApi.md#list_user_resource_access_info) | **GET** /v1/user_resource_access_info | Query various users&#39; resource access information
[**list_users**](UsersApi.md#list_users) | **GET** /users | Get all users
[**replace_challenge_method**](UsersApi.md#replace_challenge_method) | **PUT** /users/{user_id}/mfa_challenge_methods/{challenge_method_id} | Update a user&#39;s multi-factor authentication challenge method
[**replace_service_account**](UsersApi.md#replace_service_account) | **PUT** /v1/service_accounts/{service_account_id} | Update a service account
[**replace_upstream_user_identity**](UsersApi.md#replace_upstream_user_identity) | **PUT** /users/{user_id}/upstream_user_identities/{upstream_user_identity_id} | Update an upstream user identity
[**replace_user**](UsersApi.md#replace_user) | **PUT** /users/{user_id} | Create or update a user
[**replace_user_metadata**](UsersApi.md#replace_user_metadata) | **PUT** /v1/user_metadata/{metadata_id} | Update an user metadata entry.
[**replace_user_request**](UsersApi.md#replace_user_request) | **PUT** /v1/user_requests/{user_request_id} | Update an user request. Note this method ignores the state parameter.
[**replace_user_role**](UsersApi.md#replace_user_role) | **PUT** /users/{user_id}/roles | Create or update a user role
[**reset_user_mfa_challenge_methods**](UsersApi.md#reset_user_mfa_challenge_methods) | **POST** /users/{user_id}/reset_mfa_challenge_methods | Resets a user&#39;s multi-factor authentication method
[**update_user_request**](UsersApi.md#update_user_request) | **POST** /v1/user_requests/{user_request_id} | Uses the state parameter in the body to apply the action to the request


# **bulk_update_metadata**
> bulk_update_metadata()

Update a group of user's metadata for the specified org

Update a group of user's metadata for the specified org

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.bulk_user_metadata import BulkUserMetadata
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
    api_instance = users_api.UsersApi(api_client)
    bulk_user_metadata = BulkUserMetadata(
        org_id="IAsl3dl40aSsfLKiU76",
        app_id="IAsl3dl40aSsfLKiU76",
        name="name_example",
        data_type="mfa_enrollment_expiry",
        data="2002-10-02T10:00:00-05:00",
    ) # BulkUserMetadata |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a group of user's metadata for the specified org
        api_instance.bulk_update_metadata(bulk_user_metadata=bulk_user_metadata)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->bulk_update_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bulk_user_metadata** | [**BulkUserMetadata**](BulkUserMetadata.md)|  | [optional]

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
**204** | Successfully updated user metadata |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_challenge_method**
> MFAChallengeMethod create_challenge_method(user_id, mfa_challenge_method)

Create a multi-factor authentication method

Create a multi-factor authentication method

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.mfa_challenge_method import MFAChallengeMethod
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    mfa_challenge_method = MFAChallengeMethod(
        metadata=MetadataWithId(),
        spec=MFAChallengeMethodSpec(
            priority=1,
            challenge_type="challenge_type_example",
            endpoint="endpoint_example",
            origin="agilicus.cloud",
            nickname="nickname_example",
            enabled=True,
        ),
    ) # MFAChallengeMethod | 

    # example passing only required values which don't have defaults set
    try:
        # Create a multi-factor authentication method
        api_response = api_instance.create_challenge_method(user_id, mfa_challenge_method)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->create_challenge_method: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **mfa_challenge_method** | [**MFAChallengeMethod**](MFAChallengeMethod.md)|  |

### Return type

[**MFAChallengeMethod**](MFAChallengeMethod.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New authentication methods created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_service_account**
> ServiceAccount create_service_account(service_account)

Create a service account

Create a service account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.service_account import ServiceAccount
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
    api_instance = users_api.UsersApi(api_client)
    service_account = ServiceAccount(
        metadata=MetadataWithId(),
        spec=ServiceAccountSpec(
            name="ServerHealthcheck",
            enabled=True,
            org_id="IAsl3dl40aSsfLKiU76",
            allowed_sub_orgs=[
                "123",
            ],
        ),
    ) # ServiceAccount | 

    # example passing only required values which don't have defaults set
    try:
        # Create a service account
        api_response = api_instance.create_service_account(service_account)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->create_service_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_account** | [**ServiceAccount**](ServiceAccount.md)|  |

### Return type

[**ServiceAccount**](ServiceAccount.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New service account |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_upstream_user_identity**
> UpstreamUserIdentity create_upstream_user_identity(user_id, upstream_user_identity)

Create an upstream user identity

Create an upstream user identity

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.upstream_user_identity import UpstreamUserIdentity
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    upstream_user_identity = UpstreamUserIdentity(
        metadata=MetadataWithId(),
        spec=UpstreamUserIdentitySpec(
            upstream_user_id="aa-bb-cc-11-22-33",
            upstream_idp_id="https://auth.cloud.egov.city",
            local_user_id="tuU7smH86zAXMl76sua6xQ",
            attributes=UserAttributes(
                attributes=[
                    UserAttribute(
                        name="localUserId",
                        value=None,
                    ),
                ],
            ),
        ),
    ) # UpstreamUserIdentity | 

    # example passing only required values which don't have defaults set
    try:
        # Create an upstream user identity
        api_response = api_instance.create_upstream_user_identity(user_id, upstream_user_identity)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->create_upstream_user_identity: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **upstream_user_identity** | [**UpstreamUserIdentity**](UpstreamUserIdentity.md)|  |

### Return type

[**UpstreamUserIdentity**](UpstreamUserIdentity.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New upstream identity created and associated with the user. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user**
> User create_user(user)

Create a user

Create a user

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user import User
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
    api_instance = users_api.UsersApi(api_client)
    user = User() # User | 

    # example passing only required values which don't have defaults set
    try:
        # Create a user
        api_response = api_instance.create_user(user)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->create_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**User**](User.md)|  |

### Return type

[**User**](User.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New User created |  -  |
**409** | User already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_identity_update**
> UserIdentityUpdate create_user_identity_update(user_id, user_identity_update)

Update a user's core identity information.

Update a user's core identity information.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user_identity_update import UserIdentityUpdate
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    user_identity_update = UserIdentityUpdate(
        spec=UserIdentityUpdateSpec(
            primary_email=Email("foo@example.com"),
            first_name="Alice",
            last_name="Kim",
            attributes=UserAttributes(
                attributes=[
                    UserAttribute(
                        name="localUserId",
                        value=None,
                    ),
                ],
            ),
        ),
    ) # UserIdentityUpdate | 

    # example passing only required values which don't have defaults set
    try:
        # Update a user's core identity information.
        api_response = api_instance.create_user_identity_update(user_id, user_identity_update)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->create_user_identity_update: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **user_identity_update** | [**UserIdentityUpdate**](UserIdentityUpdate.md)|  |

### Return type

[**UserIdentityUpdate**](UserIdentityUpdate.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | User updated with identity information. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_metadata**
> UserMetadata create_user_metadata(user_metadata)

Create a metadata entry for the user

Create a metadata entry for the user

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user_metadata import UserMetadata
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
    api_instance = users_api.UsersApi(api_client)
    user_metadata = UserMetadata(
        metadata=MetadataWithId(),
        spec=UserMetadataSpec(
            user_id="tuU7smH86zAXMl76sua6xQ",
            org_id="IAsl3dl40aSsfLKiU76",
            app_id="IAsl3dl40aSsfLKiU76",
            name="name_example",
            data_type="mfa_enrollment_expiry",
            data="2002-10-02T10:00:00-05:00",
        ),
    ) # UserMetadata | 

    # example passing only required values which don't have defaults set
    try:
        # Create a metadata entry for the user
        api_response = api_instance.create_user_metadata(user_metadata)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->create_user_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_metadata** | [**UserMetadata**](UserMetadata.md)|  |

### Return type

[**UserMetadata**](UserMetadata.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New metadata entry created by the user |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_request**
> UserRequestInfo create_user_request(user_request_info)

Create a request on behalf of the user

Create a request on behalf of the user

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user_request_info import UserRequestInfo
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
    api_instance = users_api.UsersApi(api_client)
    user_request_info = UserRequestInfo(
        metadata=MetadataWithId(),
        spec=UserRequestInfoSpec(
            user_id="tuU7smH86zAXMl76sua6xQ",
            org_id="IAsl3dl40aSsfLKiU76",
            requested_resource="phone",
            requested_sub_resource="self",
            requested_resource_type="application_access",
            request_information="I need this to do my job",
            state="pending",
        ),
        status=UserRequestInfoStatus(
            email="foo@example.com",
        ),
    ) # UserRequestInfo | 

    # example passing only required values which don't have defaults set
    try:
        # Create a request on behalf of the user
        api_response = api_instance.create_user_request(user_request_info)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->create_user_request: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_request_info** | [**UserRequestInfo**](UserRequestInfo.md)|  |

### Return type

[**UserRequestInfo**](UserRequestInfo.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New request created by the user |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_challenge_method**
> delete_challenge_method(user_id, challenge_method_id)

Delete a user's multi-factor authentication challenge method

Delete a user's multi-factor authentication challenge method

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    challenge_method_id = "1234" # str | challenge method id

    # example passing only required values which don't have defaults set
    try:
        # Delete a user's multi-factor authentication challenge method
        api_instance.delete_challenge_method(user_id, challenge_method_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->delete_challenge_method: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **challenge_method_id** | **str**| challenge method id |

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
**204** | Challenge method updated |  -  |
**404** | Challenge method does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_service_account**
> delete_service_account(service_account_id)

Delete a service account

Delete a service account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
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
    api_instance = users_api.UsersApi(api_client)
    service_account_id = "1234" # str | service_account_id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a service account
        api_instance.delete_service_account(service_account_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->delete_service_account: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a service account
        api_instance.delete_service_account(service_account_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->delete_service_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_account_id** | **str**| service_account_id path |
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
**204** | service account was deleted |  -  |
**404** | service account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_upstream_user_identity**
> delete_upstream_user_identity(user_id, upstream_user_identity_id)

Delete an upstream user identity

Delete an upstream user identity

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    upstream_user_identity_id = "sad934lsawql2" # str | The unique id of the upstream user identity

    # example passing only required values which don't have defaults set
    try:
        # Delete an upstream user identity
        api_instance.delete_upstream_user_identity(user_id, upstream_user_identity_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->delete_upstream_user_identity: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **upstream_user_identity_id** | **str**| The unique id of the upstream user identity |

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
**204** | Upstream user identity deleted. |  -  |
**404** | Upstream user identity does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user**
> delete_user(org_id, user_id)

Remove a user from an organisation

Remove a user from an organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
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
    api_instance = users_api.UsersApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    user_id = "1234" # str | user_id path

    # example passing only required values which don't have defaults set
    try:
        # Remove a user from an organisation
        api_instance.delete_user(org_id, user_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->delete_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **user_id** | **str**| user_id path |

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
**204** | User was removed from organisation |  -  |
**404** | User does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_metadata**
> delete_user_metadata(metadata_id)

Delete an user metadata entry

Delete an user metadata entry

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
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
    api_instance = users_api.UsersApi(api_client)
    metadata_id = "1234" # str | metadata id
    user_id = "1234" # str | Query based on user id (optional)
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete an user metadata entry
        api_instance.delete_user_metadata(metadata_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->delete_user_metadata: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete an user metadata entry
        api_instance.delete_user_metadata(metadata_id, user_id=user_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->delete_user_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **metadata_id** | **str**| metadata id |
 **user_id** | **str**| Query based on user id | [optional]
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
**204** | User metadata entry deleted. |  -  |
**404** | User metadata entry does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_request**
> delete_user_request(user_request_id)

Delete an user request

Delete an user request

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
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
    api_instance = users_api.UsersApi(api_client)
    user_request_id = "1234" # str | user request id
    user_id = "1234" # str | Query based on user id (optional)
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete an user request
        api_instance.delete_user_request(user_request_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->delete_user_request: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete an user request
        api_instance.delete_user_request(user_request_id, user_id=user_id, org_id=org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->delete_user_request: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_request_id** | **str**| user request id |
 **user_id** | **str**| Query based on user id | [optional]
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
**204** | User request deleted. |  -  |
**404** | User request does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_challenge_method**
> MFAChallengeMethod get_challenge_method(user_id, challenge_method_id)

Get a single challenge method for the given user

Get a single challenge method for the given user

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.mfa_challenge_method import MFAChallengeMethod
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    challenge_method_id = "1234" # str | challenge method id

    # example passing only required values which don't have defaults set
    try:
        # Get a single challenge method for the given user
        api_response = api_instance.get_challenge_method(user_id, challenge_method_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->get_challenge_method: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **challenge_method_id** | **str**| challenge method id |

### Return type

[**MFAChallengeMethod**](MFAChallengeMethod.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return user |  -  |
**404** | Challenge method does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_service_account**
> ServiceAccount get_service_account(service_account_id)

Get a service account

Get a service account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.service_account import ServiceAccount
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
    api_instance = users_api.UsersApi(api_client)
    service_account_id = "1234" # str | service_account_id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a service account
        api_response = api_instance.get_service_account(service_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->get_service_account: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a service account
        api_response = api_instance.get_service_account(service_account_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->get_service_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_account_id** | **str**| service_account_id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**ServiceAccount**](ServiceAccount.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | service account found and returned |  -  |
**404** | service account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_upstream_user_identity**
> UpstreamUserIdentity get_upstream_user_identity(user_id, upstream_user_identity_id)

Get a single upstream user identity

Get a single upstream user identity

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.upstream_user_identity import UpstreamUserIdentity
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    upstream_user_identity_id = "sad934lsawql2" # str | The unique id of the upstream user identity

    # example passing only required values which don't have defaults set
    try:
        # Get a single upstream user identity
        api_response = api_instance.get_upstream_user_identity(user_id, upstream_user_identity_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->get_upstream_user_identity: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **upstream_user_identity_id** | **str**| The unique id of the upstream user identity |

### Return type

[**UpstreamUserIdentity**](UpstreamUserIdentity.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Upstream user identity found and returned. |  -  |
**404** | Upstream user identity does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user**
> User get_user(user_id)

Get a single user

Get a single user

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user import User
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a single user
        api_response = api_instance.get_user(user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->get_user: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single user
        api_response = api_instance.get_user(user_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->get_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**User**](User.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return user |  -  |
**404** | User does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_metadata**
> UserMetadata get_user_metadata(metadata_id)

Get a single user metadata entry

Get a single user metadata entry

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user_metadata import UserMetadata
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
    api_instance = users_api.UsersApi(api_client)
    metadata_id = "1234" # str | metadata id
    org_id = "1234" # str | Organisation Unique identifier (optional)
    user_id = "1234" # str | Query based on user id (optional)
    recursive = True # bool | If true, the query will recurse upwards (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get a single user metadata entry
        api_response = api_instance.get_user_metadata(metadata_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->get_user_metadata: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single user metadata entry
        api_response = api_instance.get_user_metadata(metadata_id, org_id=org_id, user_id=user_id, recursive=recursive)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->get_user_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **metadata_id** | **str**| metadata id |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **user_id** | **str**| Query based on user id | [optional]
 **recursive** | **bool**| If true, the query will recurse upwards | [optional] if omitted the server will use the default value of False

### Return type

[**UserMetadata**](UserMetadata.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User metadata entry found and returned |  -  |
**404** | User metadata entry does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_request**
> UserRequestInfo get_user_request(user_request_id)

Get a single user request

Get a single user request

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user_request_info import UserRequestInfo
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
    api_instance = users_api.UsersApi(api_client)
    user_request_id = "1234" # str | user request id
    org_id = "1234" # str | Organisation Unique identifier (optional)
    user_id = "1234" # str | Query based on user id (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a single user request
        api_response = api_instance.get_user_request(user_request_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->get_user_request: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single user request
        api_response = api_instance.get_user_request(user_request_id, org_id=org_id, user_id=user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->get_user_request: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_request_id** | **str**| user request id |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **user_id** | **str**| Query based on user id | [optional]

### Return type

[**UserRequestInfo**](UserRequestInfo.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User request found and returned |  -  |
**404** | User request does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_access_requests**
> ListAccessRequestsResponse list_access_requests(org_id)

Get a list of access requests

Get a list of access requests

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_access_requests_response import ListAccessRequestsResponse
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
    api_instance = users_api.UsersApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    user_id = "1234" # str | Query based on user id (optional)
    request_state = "pending" # str | The state of the request to filter the query (optional)
    request_type = "application_access" # str | The type of the request to filter the query. Note that `application_access` and `file_share_access` are deprecated. They have been replaced with `application` and `fileshare` respectively.  (optional)
    email = "foo@example.com" # str, none_type | Pagination based query with the user's email as the key. To get the initial entries supply either an empty string or null. (optional)
    search_direction = "forwards" # str | Direction which the search should go starting from the email_nullable_query parameter.  (optional) if omitted the server will use the default value of "forwards"

    # example passing only required values which don't have defaults set
    try:
        # Get a list of access requests
        api_response = api_instance.list_access_requests(org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_access_requests: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a list of access requests
        api_response = api_instance.list_access_requests(org_id, limit=limit, user_id=user_id, request_state=request_state, request_type=request_type, email=email, search_direction=search_direction)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_access_requests: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **user_id** | **str**| Query based on user id | [optional]
 **request_state** | **str**| The state of the request to filter the query | [optional]
 **request_type** | **str**| The type of the request to filter the query. Note that &#x60;application_access&#x60; and &#x60;file_share_access&#x60; are deprecated. They have been replaced with &#x60;application&#x60; and &#x60;fileshare&#x60; respectively.  | [optional]
 **email** | **str, none_type**| Pagination based query with the user&#39;s email as the key. To get the initial entries supply either an empty string or null. | [optional]
 **search_direction** | **str**| Direction which the search should go starting from the email_nullable_query parameter.  | [optional] if omitted the server will use the default value of "forwards"

### Return type

[**ListAccessRequestsResponse**](ListAccessRequestsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return user&#39;s requests |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_all_resource_permissions**
> RenderedResourcePermissions list_all_resource_permissions(user_id, org_id)

Return all per-resource permissions for a user

Retrieves the per-resource permissions for a user granted for them by the given organisation. These permissions are recursively inherted from any groups to which the user belongs. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.rendered_resource_permissions import RenderedResourcePermissions
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    org_id = "1234" # str | Organisation Unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Return all per-resource permissions for a user
        api_response = api_instance.list_all_resource_permissions(user_id, org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_all_resource_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **org_id** | **str**| Organisation Unique identifier |

### Return type

[**RenderedResourcePermissions**](RenderedResourcePermissions.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Permissions retrieved successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_all_user_orgs**
> ListOrgsResponse list_all_user_orgs(user_id)

Return all organisations a user has been assigned to

Return all organisations a user has been assigned to

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    issuer = "example.com" # str | Organisation issuer (optional)

    # example passing only required values which don't have defaults set
    try:
        # Return all organisations a user has been assigned to
        api_response = api_instance.list_all_user_orgs(user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_all_user_orgs: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Return all organisations a user has been assigned to
        api_response = api_instance.list_all_user_orgs(user_id, issuer=issuer)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_all_user_orgs: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **issuer** | **str**| Organisation issuer | [optional]

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
**200** | roles |  -  |
**404** | User does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_all_user_roles**
> Roles list_all_user_roles(user_id)

Return all roles for a user

Retrieves the roles (application and api) for a user granted for them by the given organisation. These permissions are recursively inherted from any groups to which the user belongs. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.roles import Roles
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Return all roles for a user
        api_response = api_instance.list_all_user_roles(user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_all_user_roles: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Return all roles for a user
        api_response = api_instance.list_all_user_roles(user_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_all_user_roles: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**Roles**](Roles.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | roles |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_challenge_methods**
> ListMFAChallengeMethods list_challenge_methods(user_id)

Get all of a user's multi-factor authentication challenge method configuration

Get all of a user's multi-factor authentication challenge method configuration

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_mfa_challenge_methods import ListMFAChallengeMethods
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    challenge_type = "sms" # str | challenge method type query (optional)
    method_status = False # bool | The status of the challenge method. True for enabled, false for disabled. (optional)
    method_origin = "agilicus.cloud" # str | The origin of a challenge method (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all of a user's multi-factor authentication challenge method configuration
        api_response = api_instance.list_challenge_methods(user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_challenge_methods: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all of a user's multi-factor authentication challenge method configuration
        api_response = api_instance.list_challenge_methods(user_id, limit=limit, challenge_type=challenge_type, method_status=method_status, method_origin=method_origin)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_challenge_methods: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **challenge_type** | **str**| challenge method type query | [optional]
 **method_status** | **bool**| The status of the challenge method. True for enabled, false for disabled. | [optional]
 **method_origin** | **str**| The origin of a challenge method | [optional]

### Return type

[**ListMFAChallengeMethods**](ListMFAChallengeMethods.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return user&#39;s multi-factor authentication challenge method configuration |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_combined_user_details**
> ListCombinedUserDetailsResponse list_combined_user_details()

Get all combined details about users

Get all combined details about users

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_combined_user_details_response import ListCombinedUserDetailsResponse
from agilicus_api.model.user_status_enum import UserStatusEnum
from agilicus_api.model.email import Email
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
    api_instance = users_api.UsersApi(api_client)
    email = Email("foo@example.com") # Email | Query based on user email (optional)
    previous_email = Email("foo@example.com") # Email | Pagination based query with the user's email as the key. To get the initial entries supply an empty string. (optional)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    type = "1234" # str | user type (optional)
    user_id = "1234" # str | Query based on user id (optional)
    status = [
        UserStatusEnum("["active"]"),
    ] # [UserStatusEnum] | The status of users to search for. Multiple values are ORed together. (optional)
    mfa_enrolled = True # bool | Restrict query based on the mfa enrollment status of users. Can be omitted for no query restriction. If true, only get users with at least one mfa challenge method. If false, only get users without any mfa challenge methods.  (optional)
    auto_created = True # bool | Restrict query based on auto-creation. Can be omitted to get all users with no restriction. If true, only get users that are in the auto-created-users group. If false, only get users that are not in the auto-created-users group.  (optional)
    search_direction = "forwards" # str | Direction which the search should go starting from the email_nullable_query parameter.  (optional) if omitted the server will use the default value of "forwards"
    prefix_email_search = Email("Foo") # Email | Keyword used to search for a list of users based on email. This parameter is case insensitive and finds users with an email that matches the keyword by its prefix. For example, if the keyword \"Foo\" is supplied to this parameter, users with emails of \"foo1@example.com\" and \"Foo2@test.com\" could be returned.  (optional)
    allow_partial_match = True # bool | Perform a case insensitive partial match of any string query parameters included in the query  (optional)
    first_name = "John" # str | query for users with a first name that matches the query parameter (optional)
    last_name = "Smith" # str | query for users with a last name that matches the query parameter (optional)
    search_params = [
        "mat",
    ] # [str] | A list of strings to perform a case-insensitive search on all relevant fields in the database for a given collection. Multiple values are ANDed together  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all combined details about users
        api_response = api_instance.list_combined_user_details(email=email, previous_email=previous_email, org_id=org_id, limit=limit, type=type, user_id=user_id, status=status, mfa_enrolled=mfa_enrolled, auto_created=auto_created, search_direction=search_direction, prefix_email_search=prefix_email_search, allow_partial_match=allow_partial_match, first_name=first_name, last_name=last_name, search_params=search_params)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_combined_user_details: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **email** | **Email**| Query based on user email | [optional]
 **previous_email** | **Email**| Pagination based query with the user&#39;s email as the key. To get the initial entries supply an empty string. | [optional]
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **type** | **str**| user type | [optional]
 **user_id** | **str**| Query based on user id | [optional]
 **status** | [**[UserStatusEnum]**](UserStatusEnum.md)| The status of users to search for. Multiple values are ORed together. | [optional]
 **mfa_enrolled** | **bool**| Restrict query based on the mfa enrollment status of users. Can be omitted for no query restriction. If true, only get users with at least one mfa challenge method. If false, only get users without any mfa challenge methods.  | [optional]
 **auto_created** | **bool**| Restrict query based on auto-creation. Can be omitted to get all users with no restriction. If true, only get users that are in the auto-created-users group. If false, only get users that are not in the auto-created-users group.  | [optional]
 **search_direction** | **str**| Direction which the search should go starting from the email_nullable_query parameter.  | [optional] if omitted the server will use the default value of "forwards"
 **prefix_email_search** | **Email**| Keyword used to search for a list of users based on email. This parameter is case insensitive and finds users with an email that matches the keyword by its prefix. For example, if the keyword \&quot;Foo\&quot; is supplied to this parameter, users with emails of \&quot;foo1@example.com\&quot; and \&quot;Foo2@test.com\&quot; could be returned.  | [optional]
 **allow_partial_match** | **bool**| Perform a case insensitive partial match of any string query parameters included in the query  | [optional]
 **first_name** | **str**| query for users with a first name that matches the query parameter | [optional]
 **last_name** | **str**| query for users with a last name that matches the query parameter | [optional]
 **search_params** | **[str]**| A list of strings to perform a case-insensitive search on all relevant fields in the database for a given collection. Multiple values are ANDed together  | [optional]

### Return type

[**ListCombinedUserDetailsResponse**](ListCombinedUserDetailsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return combined user details |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_desktop_access_info**
> ListUserDesktopAccessInfoResponse list_desktop_access_info(org_id, user_id)

Query various users' desktop access information

Query various users' desktop access information

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.selector_tag import SelectorTag
from agilicus_api.model.list_user_desktop_access_info_response import ListUserDesktopAccessInfoResponse
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
    api_instance = users_api.UsersApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    user_id = "1234" # str | Query based on user id
    tag = [
        SelectorTag("theme"),
    ] # [SelectorTag] | Search files based on tag (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    desktop_type = "rdp" # str | The type of desktop search for. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Query various users' desktop access information
        api_response = api_instance.list_desktop_access_info(org_id, user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_desktop_access_info: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Query various users' desktop access information
        api_response = api_instance.list_desktop_access_info(org_id, user_id, tag=tag, limit=limit, desktop_type=desktop_type)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_desktop_access_info: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **user_id** | **str**| Query based on user id |
 **tag** | [**[SelectorTag]**](SelectorTag.md)| Search files based on tag | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **desktop_type** | **str**| The type of desktop search for. | [optional]

### Return type

[**ListUserDesktopAccessInfoResponse**](ListUserDesktopAccessInfoResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved UserDesktopAccessInfo |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_org_user_roles**
> ListUserRolesForAnOrg list_org_user_roles()

Get all org user roles

Get all org user roles

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_user_roles_for_an_org import ListUserRolesForAnOrg
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
    api_instance = users_api.UsersApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    user_id = "1234" # str | Query based on user id (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    offset = 0 # int | An offset into the set of data to be returned. This is used for pagination. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all org user roles
        api_response = api_instance.list_org_user_roles(org_id=org_id, user_id=user_id, limit=limit, offset=offset)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_org_user_roles: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **user_id** | **str**| Query based on user id | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **offset** | **int**| An offset into the set of data to be returned. This is used for pagination. | [optional]

### Return type

[**ListUserRolesForAnOrg**](ListUserRolesForAnOrg.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return org user roles |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_service_accounts**
> ListServiceAccountResponse list_service_accounts()

List service accounts

List service accounts

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_service_account_response import ListServiceAccountResponse
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
    api_instance = users_api.UsersApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    user_id = "1234" # str | Query based on user id (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List service accounts
        api_response = api_instance.list_service_accounts(org_id=org_id, user_id=user_id, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_service_accounts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **user_id** | **str**| Query based on user id | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListServiceAccountResponse**](ListServiceAccountResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of service accounts. The query can be limited to all service accounts owned by a specific organisation or can be used to look up the service account associated with an user id.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_upstream_user_identities**
> ListUpstreamUserIdentitiesResponse list_upstream_user_identities(user_id)

Get all of a user's upstream user identities

Get all of a user's upstream user identities

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_upstream_user_identities_response import ListUpstreamUserIdentitiesResponse
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    try:
        # Get all of a user's upstream user identities
        api_response = api_instance.list_upstream_user_identities(user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_upstream_user_identities: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all of a user's upstream user identities
        api_response = api_instance.list_upstream_user_identities(user_id, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_upstream_user_identities: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListUpstreamUserIdentitiesResponse**](ListUpstreamUserIdentitiesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return user&#39;s upstream identities |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_user_application_access_info**
> ListUserApplicationAccessInfoResponse list_user_application_access_info(org_id, user_id)

Query various users' application access information

Query various users' application access information

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_user_application_access_info_response import ListUserApplicationAccessInfoResponse
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
    api_instance = users_api.UsersApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    user_id = "1234" # str | Query based on user id
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    try:
        # Query various users' application access information
        api_response = api_instance.list_user_application_access_info(org_id, user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_application_access_info: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Query various users' application access information
        api_response = api_instance.list_user_application_access_info(org_id, user_id, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_application_access_info: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **user_id** | **str**| Query based on user id |
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListUserApplicationAccessInfoResponse**](ListUserApplicationAccessInfoResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved UserApplicationAccessInfo |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_user_file_share_access_info**
> ListUserFileShareAccessInfoResponse list_user_file_share_access_info(org_id, user_id)

Query various users' file share access information

Query various users' file share access information

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.selector_tag import SelectorTag
from agilicus_api.model.list_user_file_share_access_info_response import ListUserFileShareAccessInfoResponse
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
    api_instance = users_api.UsersApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    user_id = "1234" # str | Query based on user id
    tag = [
        SelectorTag("theme"),
    ] # [SelectorTag] | Search files based on tag (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    try:
        # Query various users' file share access information
        api_response = api_instance.list_user_file_share_access_info(org_id, user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_file_share_access_info: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Query various users' file share access information
        api_response = api_instance.list_user_file_share_access_info(org_id, user_id, tag=tag, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_file_share_access_info: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **user_id** | **str**| Query based on user id |
 **tag** | [**[SelectorTag]**](SelectorTag.md)| Search files based on tag | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListUserFileShareAccessInfoResponse**](ListUserFileShareAccessInfoResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved UserFileShareAccessInfo |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_user_guid_mapping**
> ListGuidMetadataResponse list_user_guid_mapping()

Get all user guids and a unique name mapping

Get all user guids and a unique name mapping

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
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
    api_instance = users_api.UsersApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    user_id = "1234" # str | Query based on user id (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    previous_guid = "73WakrfVbNJBaAmhQtEeDv" # str | Pagination based query with the guid as the key. To get the initial entries supply an empty string. (optional)
    updated_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | query since updated (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all user guids and a unique name mapping
        api_response = api_instance.list_user_guid_mapping(org_id=org_id, user_id=user_id, limit=limit, previous_guid=previous_guid, updated_since=updated_since)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_guid_mapping: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **user_id** | **str**| Query based on user id | [optional]
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

# **list_user_guids**
> ListUserGuidsResponse list_user_guids()

Get a list of all user GUIDs

Get a list of all user GUIDs

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_user_guids_response import ListUserGuidsResponse
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
    api_instance = users_api.UsersApi(api_client)
    updated_since = dateutil_parser('2015-07-07T15:49:51.230+02:00') # datetime | query since updated (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a list of all user GUIDs
        api_response = api_instance.list_user_guids(updated_since=updated_since)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_guids: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **updated_since** | **datetime**| query since updated | [optional]

### Return type

[**ListUserGuidsResponse**](ListUserGuidsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of user GUIDs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_user_launcher_access_info**
> ListUserLauncherAccessInfoResponse list_user_launcher_access_info(org_id, user_id)

Query various users' launchers access information

Query various users' launchers access information

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_user_launcher_access_info_response import ListUserLauncherAccessInfoResponse
from agilicus_api.model.selector_tag import SelectorTag
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
    api_instance = users_api.UsersApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    user_id = "1234" # str | Query based on user id
    tag = [
        SelectorTag("theme"),
    ] # [SelectorTag] | Search files based on tag (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    try:
        # Query various users' launchers access information
        api_response = api_instance.list_user_launcher_access_info(org_id, user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_launcher_access_info: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Query various users' launchers access information
        api_response = api_instance.list_user_launcher_access_info(org_id, user_id, tag=tag, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_launcher_access_info: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **user_id** | **str**| Query based on user id |
 **tag** | [**[SelectorTag]**](SelectorTag.md)| Search files based on tag | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListUserLauncherAccessInfoResponse**](ListUserLauncherAccessInfoResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved UserLauncherAccessInfo |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_user_metadata**
> ListUserMetadataResponse list_user_metadata()

Get a list of user metadata entries

Get a list of user metadata entries

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_user_metadata_response import ListUserMetadataResponse
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
    api_instance = users_api.UsersApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    user_id = "1234" # str | Query based on user id (optional)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    app_id = "G" # str | Application unique identifier (optional)
    data_type = "mfa_enrollment_expiry" # str | The data type of the metadata (optional)
    recursive = True # bool | If true, the query will recurse upwards (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a list of user metadata entries
        api_response = api_instance.list_user_metadata(limit=limit, user_id=user_id, org_id=org_id, app_id=app_id, data_type=data_type, recursive=recursive)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **user_id** | **str**| Query based on user id | [optional]
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **app_id** | **str**| Application unique identifier | [optional]
 **data_type** | **str**| The data type of the metadata | [optional]
 **recursive** | **bool**| If true, the query will recurse upwards | [optional] if omitted the server will use the default value of False

### Return type

[**ListUserMetadataResponse**](ListUserMetadataResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return user metadata entries |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_user_permissions**
> HostPermissions list_user_permissions(user_id)

Return the user's host permissions

Return the user's host permissions

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.host_permissions import HostPermissions
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    try:
        # Return the user's host permissions
        api_response = api_instance.list_user_permissions(user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_permissions: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Return the user's host permissions
        api_response = api_instance.list_user_permissions(user_id, org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**HostPermissions**](HostPermissions.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | roles |  -  |
**404** | User does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_user_requests**
> ListUserRequestInfoResponse list_user_requests()

Get a list of user requests

Get a list of user requests

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.list_user_request_info_response import ListUserRequestInfoResponse
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
    api_instance = users_api.UsersApi(api_client)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    user_id = "1234" # str | Query based on user id (optional)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    request_state = "pending" # str | The state of the request to filter the query (optional)
    request_type = "application_access" # str | The type of the request to filter the query. Note that `application_access` and `file_share_access` are deprecated. They have been replaced with `application` and `fileshare` respectively.  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a list of user requests
        api_response = api_instance.list_user_requests(limit=limit, user_id=user_id, org_id=org_id, request_state=request_state, request_type=request_type)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_requests: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **user_id** | **str**| Query based on user id | [optional]
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **request_state** | **str**| The state of the request to filter the query | [optional]
 **request_type** | **str**| The type of the request to filter the query. Note that &#x60;application_access&#x60; and &#x60;file_share_access&#x60; are deprecated. They have been replaced with &#x60;application&#x60; and &#x60;fileshare&#x60; respectively.  | [optional]

### Return type

[**ListUserRequestInfoResponse**](ListUserRequestInfoResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return user&#39;s requests |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_user_resource_access_info**
> ListUserResourceAccessInfoResponse list_user_resource_access_info(org_id, user_id)

Query various users' resource access information

Query various users' resource access information

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.selector_tag import SelectorTag
from agilicus_api.model.list_user_resource_access_info_response import ListUserResourceAccessInfoResponse
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
    api_instance = users_api.UsersApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier
    user_id = "1234" # str | Query based on user id
    resource_type = "fileshare" # str | The type of resource to query for (optional)
    tag = [
        SelectorTag("theme"),
    ] # [SelectorTag] | Search files based on tag (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500

    # example passing only required values which don't have defaults set
    try:
        # Query various users' resource access information
        api_response = api_instance.list_user_resource_access_info(org_id, user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_resource_access_info: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Query various users' resource access information
        api_response = api_instance.list_user_resource_access_info(org_id, user_id, resource_type=resource_type, tag=tag, limit=limit)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_user_resource_access_info: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier |
 **user_id** | **str**| Query based on user id |
 **resource_type** | **str**| The type of resource to query for | [optional]
 **tag** | [**[SelectorTag]**](SelectorTag.md)| Search files based on tag | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500

### Return type

[**ListUserResourceAccessInfoResponse**](ListUserResourceAccessInfoResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved UserResourceAccessInfo |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_users**
> ListUsersResponse list_users()

Get all users

Get all users

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user_status_enum import UserStatusEnum
from agilicus_api.model.list_users_response import ListUsersResponse
from agilicus_api.model.email import Email
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
    api_instance = users_api.UsersApi(api_client)
    email = Email("foo@example.com") # Email | Query based on user email (optional)
    previous_email = Email("foo@example.com") # Email | Pagination based query with the user's email as the key. To get the initial entries supply an empty string. (optional)
    provider = "google.com" # str | Query based on identity provider (optional)
    org_id = "1234" # str | Organisation Unique identifier (optional)
    issuer = "example.com" # str | Organisation issuer (optional)
    limit = 1 # int | limit the number of rows in the response (optional) if omitted the server will use the default value of 500
    type = ["user"] # [str] | The type of users to search for. Multiple values are ORed together. (optional)
    upstream_user_id = "1234-abcd" # str | The id of the user from upstream (optional)
    upstream_idp_id = "sad934lsawql2" # str | The unique id of the upstream idp (optional)
    status = [
        UserStatusEnum("["active"]"),
    ] # [UserStatusEnum] | The status of users to search for. Multiple values are ORed together. (optional)
    search_direction = "forwards" # str | Direction which the search should go starting from the email_nullable_query parameter.  (optional) if omitted the server will use the default value of "forwards"
    has_roles = True # bool | Restrict query based on user permissions. Can be omitted to get all users with no restriction. If true, only get users that have at least one role. If false, only get users with no roles.  (optional)
    has_resource_roles = True # bool | Restrict query based on user resource permissions. Can be omitted to get all users with no resource restriction. If true, only get users that have at least one resource role. If false, only get users with no resource roles.  (optional)
    prefix_email_search = Email("Foo") # Email | Keyword used to search for a list of users based on email. This parameter is case insensitive and finds users with an email that matches the keyword by its prefix. For example, if the keyword \"Foo\" is supplied to this parameter, users with emails of \"foo1@example.com\" and \"Foo2@test.com\" could be returned.  (optional)
    orgless_users = True # bool | Filter for all users that do not have an org associated with them (optional)
    allow_partial_match = True # bool | Perform a case insensitive partial match of any string query parameters included in the query  (optional)
    first_name = "John" # str | query for users with a first name that matches the query parameter (optional)
    last_name = "Smith" # str | query for users with a last name that matches the query parameter (optional)
    user_id = "1234" # str | Query based on user id (optional)
    search_params = [
        "mat",
    ] # [str] | A list of strings to perform a case-insensitive search on all relevant fields in the database for a given collection. Multiple values are ANDed together  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all users
        api_response = api_instance.list_users(email=email, previous_email=previous_email, provider=provider, org_id=org_id, issuer=issuer, limit=limit, type=type, upstream_user_id=upstream_user_id, upstream_idp_id=upstream_idp_id, status=status, search_direction=search_direction, has_roles=has_roles, has_resource_roles=has_resource_roles, prefix_email_search=prefix_email_search, orgless_users=orgless_users, allow_partial_match=allow_partial_match, first_name=first_name, last_name=last_name, user_id=user_id, search_params=search_params)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->list_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **email** | **Email**| Query based on user email | [optional]
 **previous_email** | **Email**| Pagination based query with the user&#39;s email as the key. To get the initial entries supply an empty string. | [optional]
 **provider** | **str**| Query based on identity provider | [optional]
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **issuer** | **str**| Organisation issuer | [optional]
 **limit** | **int**| limit the number of rows in the response | [optional] if omitted the server will use the default value of 500
 **type** | **[str]**| The type of users to search for. Multiple values are ORed together. | [optional]
 **upstream_user_id** | **str**| The id of the user from upstream | [optional]
 **upstream_idp_id** | **str**| The unique id of the upstream idp | [optional]
 **status** | [**[UserStatusEnum]**](UserStatusEnum.md)| The status of users to search for. Multiple values are ORed together. | [optional]
 **search_direction** | **str**| Direction which the search should go starting from the email_nullable_query parameter.  | [optional] if omitted the server will use the default value of "forwards"
 **has_roles** | **bool**| Restrict query based on user permissions. Can be omitted to get all users with no restriction. If true, only get users that have at least one role. If false, only get users with no roles.  | [optional]
 **has_resource_roles** | **bool**| Restrict query based on user resource permissions. Can be omitted to get all users with no resource restriction. If true, only get users that have at least one resource role. If false, only get users with no resource roles.  | [optional]
 **prefix_email_search** | **Email**| Keyword used to search for a list of users based on email. This parameter is case insensitive and finds users with an email that matches the keyword by its prefix. For example, if the keyword \&quot;Foo\&quot; is supplied to this parameter, users with emails of \&quot;foo1@example.com\&quot; and \&quot;Foo2@test.com\&quot; could be returned.  | [optional]
 **orgless_users** | **bool**| Filter for all users that do not have an org associated with them | [optional]
 **allow_partial_match** | **bool**| Perform a case insensitive partial match of any string query parameters included in the query  | [optional]
 **first_name** | **str**| query for users with a first name that matches the query parameter | [optional]
 **last_name** | **str**| query for users with a last name that matches the query parameter | [optional]
 **user_id** | **str**| Query based on user id | [optional]
 **search_params** | **[str]**| A list of strings to perform a case-insensitive search on all relevant fields in the database for a given collection. Multiple values are ANDed together  | [optional]

### Return type

[**ListUsersResponse**](ListUsersResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return users |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_challenge_method**
> MFAChallengeMethod replace_challenge_method(user_id, challenge_method_id)

Update a user's multi-factor authentication challenge method

Update a user's multi-factor authentication challenge method

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.mfa_challenge_method import MFAChallengeMethod
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    challenge_method_id = "1234" # str | challenge method id
    mfa_challenge_method = MFAChallengeMethod(
        metadata=MetadataWithId(),
        spec=MFAChallengeMethodSpec(
            priority=1,
            challenge_type="challenge_type_example",
            endpoint="endpoint_example",
            origin="agilicus.cloud",
            nickname="nickname_example",
            enabled=True,
        ),
    ) # MFAChallengeMethod |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a user's multi-factor authentication challenge method
        api_response = api_instance.replace_challenge_method(user_id, challenge_method_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_challenge_method: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a user's multi-factor authentication challenge method
        api_response = api_instance.replace_challenge_method(user_id, challenge_method_id, mfa_challenge_method=mfa_challenge_method)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_challenge_method: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **challenge_method_id** | **str**| challenge method id |
 **mfa_challenge_method** | [**MFAChallengeMethod**](MFAChallengeMethod.md)|  | [optional]

### Return type

[**MFAChallengeMethod**](MFAChallengeMethod.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Challenge method updated |  -  |
**404** | Challenge method does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_service_account**
> ServiceAccount replace_service_account(service_account_id)

Update a service account

Update a service account

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.service_account import ServiceAccount
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
    api_instance = users_api.UsersApi(api_client)
    service_account_id = "1234" # str | service_account_id path
    service_account = ServiceAccount(
        metadata=MetadataWithId(),
        spec=ServiceAccountSpec(
            name="ServerHealthcheck",
            enabled=True,
            org_id="IAsl3dl40aSsfLKiU76",
            allowed_sub_orgs=[
                "123",
            ],
        ),
    ) # ServiceAccount |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a service account
        api_response = api_instance.replace_service_account(service_account_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_service_account: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a service account
        api_response = api_instance.replace_service_account(service_account_id, service_account=service_account)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_service_account: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_account_id** | **str**| service_account_id path |
 **service_account** | [**ServiceAccount**](ServiceAccount.md)|  | [optional]

### Return type

[**ServiceAccount**](ServiceAccount.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | service account updated |  -  |
**404** | service account does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_upstream_user_identity**
> UpstreamUserIdentity replace_upstream_user_identity(user_id, upstream_user_identity_id)

Update an upstream user identity

Update an upstream user identity

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.upstream_user_identity import UpstreamUserIdentity
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    upstream_user_identity_id = "sad934lsawql2" # str | The unique id of the upstream user identity
    upstream_user_identity = UpstreamUserIdentity(
        metadata=MetadataWithId(),
        spec=UpstreamUserIdentitySpec(
            upstream_user_id="aa-bb-cc-11-22-33",
            upstream_idp_id="https://auth.cloud.egov.city",
            local_user_id="tuU7smH86zAXMl76sua6xQ",
            attributes=UserAttributes(
                attributes=[
                    UserAttribute(
                        name="localUserId",
                        value=None,
                    ),
                ],
            ),
        ),
    ) # UpstreamUserIdentity |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update an upstream user identity
        api_response = api_instance.replace_upstream_user_identity(user_id, upstream_user_identity_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_upstream_user_identity: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update an upstream user identity
        api_response = api_instance.replace_upstream_user_identity(user_id, upstream_user_identity_id, upstream_user_identity=upstream_user_identity)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_upstream_user_identity: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **upstream_user_identity_id** | **str**| The unique id of the upstream user identity |
 **upstream_user_identity** | [**UpstreamUserIdentity**](UpstreamUserIdentity.md)|  | [optional]

### Return type

[**UpstreamUserIdentity**](UpstreamUserIdentity.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Upstream user identity updated |  -  |
**404** | Upstream user identity does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_user**
> User replace_user(user_id)

Create or update a user

Create or update a user

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user import User
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    user = User() # User |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a user
        api_response = api_instance.replace_user(user_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_user: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a user
        api_response = api_instance.replace_user(user_id, user=user)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **user** | [**User**](User.md)|  | [optional]

### Return type

[**User**](User.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated user |  -  |
**404** | User does not exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_user_metadata**
> UserMetadata replace_user_metadata(metadata_id)

Update an user metadata entry.

Update an user metadata entry.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user_metadata import UserMetadata
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
    api_instance = users_api.UsersApi(api_client)
    metadata_id = "1234" # str | metadata id
    user_metadata = UserMetadata(
        metadata=MetadataWithId(),
        spec=UserMetadataSpec(
            user_id="tuU7smH86zAXMl76sua6xQ",
            org_id="IAsl3dl40aSsfLKiU76",
            app_id="IAsl3dl40aSsfLKiU76",
            name="name_example",
            data_type="mfa_enrollment_expiry",
            data="2002-10-02T10:00:00-05:00",
        ),
    ) # UserMetadata |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update an user metadata entry.
        api_response = api_instance.replace_user_metadata(metadata_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_user_metadata: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update an user metadata entry.
        api_response = api_instance.replace_user_metadata(metadata_id, user_metadata=user_metadata)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_user_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **metadata_id** | **str**| metadata id |
 **user_metadata** | [**UserMetadata**](UserMetadata.md)|  | [optional]

### Return type

[**UserMetadata**](UserMetadata.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User metadata entry info updated |  -  |
**404** | User metadata entry does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_user_request**
> UserRequestInfo replace_user_request(user_request_id)

Update an user request. Note this method ignores the state parameter.

Update an user request. Note this method ignores the state parameter.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user_request_info import UserRequestInfo
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
    api_instance = users_api.UsersApi(api_client)
    user_request_id = "1234" # str | user request id
    user_request_info = UserRequestInfo(
        metadata=MetadataWithId(),
        spec=UserRequestInfoSpec(
            user_id="tuU7smH86zAXMl76sua6xQ",
            org_id="IAsl3dl40aSsfLKiU76",
            requested_resource="phone",
            requested_sub_resource="self",
            requested_resource_type="application_access",
            request_information="I need this to do my job",
            state="pending",
        ),
        status=UserRequestInfoStatus(
            email="foo@example.com",
        ),
    ) # UserRequestInfo |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update an user request. Note this method ignores the state parameter.
        api_response = api_instance.replace_user_request(user_request_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_user_request: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update an user request. Note this method ignores the state parameter.
        api_response = api_instance.replace_user_request(user_request_id, user_request_info=user_request_info)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_user_request: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_request_id** | **str**| user request id |
 **user_request_info** | [**UserRequestInfo**](UserRequestInfo.md)|  | [optional]

### Return type

[**UserRequestInfo**](UserRequestInfo.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User request info updated |  -  |
**404** | User request does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_user_role**
> replace_user_role(user_id)

Create or update a user role

Create or update a user role

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.replace_user_role_request import ReplaceUserRoleRequest
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    org_id = "1234" # str | Organisation Unique identifier (optional)
    replace_user_role_request = ReplaceUserRoleRequest(
        roles=Roles(
            key=[
                "key_example",
            ],
        ),
    ) # ReplaceUserRoleRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a user role
        api_instance.replace_user_role(user_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_user_role: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a user role
        api_instance.replace_user_role(user_id, org_id=org_id, replace_user_role_request=replace_user_role_request)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->replace_user_role: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **org_id** | **str**| Organisation Unique identifier | [optional]
 **replace_user_role_request** | [**ReplaceUserRoleRequest**](ReplaceUserRoleRequest.md)|  | [optional]

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
**204** | User role updated |  -  |
**404** | User does not exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_user_mfa_challenge_methods**
> reset_user_mfa_challenge_methods(user_id, reset_mfa_challenge_method)

Resets a user's multi-factor authentication method

Resets a user's multi-factor authentication method

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.reset_mfa_challenge_method import ResetMFAChallengeMethod
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
    api_instance = users_api.UsersApi(api_client)
    user_id = "1234" # str | user_id path
    reset_mfa_challenge_method = ResetMFAChallengeMethod(
        org_id="123",
    ) # ResetMFAChallengeMethod | 

    # example passing only required values which don't have defaults set
    try:
        # Resets a user's multi-factor authentication method
        api_instance.reset_user_mfa_challenge_methods(user_id, reset_mfa_challenge_method)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->reset_user_mfa_challenge_methods: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path |
 **reset_mfa_challenge_method** | [**ResetMFAChallengeMethod**](ResetMFAChallengeMethod.md)|  |

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
**204** | User&#39;s multi-factor authentication methods were reset successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_request**
> UserRequestInfo update_user_request(user_request_id)

Uses the state parameter in the body to apply the action to the request

Uses the state parameter in the body to apply the action to the request

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import users_api
from agilicus_api.model.user_request_info import UserRequestInfo
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
    api_instance = users_api.UsersApi(api_client)
    user_request_id = "1234" # str | user request id
    user_request_info = UserRequestInfo(
        metadata=MetadataWithId(),
        spec=UserRequestInfoSpec(
            user_id="tuU7smH86zAXMl76sua6xQ",
            org_id="IAsl3dl40aSsfLKiU76",
            requested_resource="phone",
            requested_sub_resource="self",
            requested_resource_type="application_access",
            request_information="I need this to do my job",
            state="pending",
        ),
        status=UserRequestInfoStatus(
            email="foo@example.com",
        ),
    ) # UserRequestInfo |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Uses the state parameter in the body to apply the action to the request
        api_response = api_instance.update_user_request(user_request_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->update_user_request: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Uses the state parameter in the body to apply the action to the request
        api_response = api_instance.update_user_request(user_request_id, user_request_info=user_request_info)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling UsersApi->update_user_request: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_request_id** | **str**| user request id |
 **user_request_info** | [**UserRequestInfo**](UserRequestInfo.md)|  | [optional]

### Return type

[**UserRequestInfo**](UserRequestInfo.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User request info updated |  -  |
**404** | User request does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

