# FileShareServiceStatus

Derived, read-only properties of a FileShareService. Use these to determine how to interact with a file share service, or the current state of the file share service. Note that if service is not assigned to anything, it will have no host-related information. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**share_base_app_name** | **str** | The name of the application in the system providing the file share. This can be used to construct the default URI used to access the file share given the organisation&#39;s subdomain.  | [optional] 
**instance_id** | **str** | The identifier of the instance running the file share. Useful for auditing/etc.  | [optional] 
**instance_org_id** | **str** | The identifier of the organistion responsible for the instance running the file share.  | [optional] 
**share_uri** | **str** | The uri at which to access this file share. If this value is empty, the file share can be accessed at https://shares.$(organisation.subdomain)/share_name.  | [optional] 
**stats** | [**FileShareServiceStats**](FileShareServiceStats.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


