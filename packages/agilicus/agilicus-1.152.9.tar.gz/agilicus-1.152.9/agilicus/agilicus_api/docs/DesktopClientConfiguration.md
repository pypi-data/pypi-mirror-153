# DesktopClientConfiguration

Contains the information usd to generate a configuration file for a client wishing to access a DesktopResource, as well that configuration file itself. The system generates the configuration file when the DesktopClientConfiguration is created. Set the `user_id` to provide credentials for the user in the generated configuration. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_id** | **str** | The ID of the organisation which owns this DesktopClient.  | 
**user_id** | **str, none_type** | The ID of the user wishing to access this DesktopResource. If this field is not set, no credentials will be provided in the DesktopClientGeneratedConfiguration.  | [optional] 
**generated_config** | [**DesktopClientGeneratedConfiguration**](DesktopClientGeneratedConfiguration.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


