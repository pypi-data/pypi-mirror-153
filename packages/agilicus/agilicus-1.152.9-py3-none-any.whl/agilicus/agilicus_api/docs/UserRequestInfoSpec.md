# UserRequestInfoSpec

The specification for an user request

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | The unique id of the User to which this record applies.  | 
**org_id** | **str** | The unique id of the Organisation to which this record applies.  | 
**requested_resource** | **str** | The resource the user is requesting. For example an application name if the request_type is application. If the request_type is fileshare, this would be the file share name.  | 
**requested_resource_type** | **str** | The type of request a user is making. Note that &#x60;application_access&#x60; and &#x60;file_share_access&#x60; are deprecated. They have been replaced with &#x60;application&#x60; and &#x60;fileshare&#x60; respectively.  | 
**requested_sub_resource** | **str** | A resource tied to the resource the user is requesting. For example, this could be the name of a role if the request_type is application_access.  | [optional] 
**request_information** | **str** | Text describing why the user is requesting application access | [optional] 
**state** | **str** | The state of the resource access request | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


