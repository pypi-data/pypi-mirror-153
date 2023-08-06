# OperationalStatus

The Operational Status for an Entity. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | The status can have the following values: - A &#x60;good&#x60; status means that no action is neccessary - A &#x60;down&#x60; status indicates that there is a service accessibility problem   that should be dealt with as soon as possible.  | 
**status_change_time** | **datetime** | The data and time when the status changed in value. | [optional] 
**generation** | **int** | The generation count is incremented periodically by the system as it monitors and verifies the current status.  | [optional] 
**generation_update_time** | **datetime** | The data and time when the generation count was last updated. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


