# ServiceForwarderSpec

The configurable properties of a ServiceForwarder. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the service forwarder. This value must be unique within an organisation.  | 
**org_id** | **str** | The organisation which owns this service forwarder. | 
**port** | **int** | The transport-layer port on which to access the service forwarder. exclusiveMinimum: 0 exclusiveMaximum: 65536  | 
**application_service_id** | **str** | The application service id that this service forwarder connects to.  | 
**connector_id** | **str** | Unique identifier | 
**bind_address** | **str** | The local bind address that local applications will forward to in order to access the service forwarder.  bind_address default is localhost.  | [optional] 
**protocol** | **str** | The transport-layer protocol being fowarded to the remote application service.  | [optional]  if omitted the server will use the default value of "tcp"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


