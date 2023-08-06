# ApplicationServiceRoute

An application service route defines how a service, which is associated to an application, is routed internally. This would be based upon how the service is assigned (the ApplicationServiceAssignment), and its expose_type.  For a service route, it is expected that an external name and/or path_prefix would route to an internal_name.  Examples:     external_name -> internal_name     external_name/path_prefix -> internal_name     application_external_name/path_prefix -> internal_name 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_id** | **str** | Unique identifier | [readonly] 
**internal_name** | **str** | The internal name of the service.  | 
**protocol_config** | [**ServiceProtocolConfig**](ServiceProtocolConfig.md) |  | [optional] 
**path_prefix** | **str** | The URL path prefix should service routing be achieved by using a path prefix.  | [optional] 
**external_name** | **str** | The external name of the service. If the field is nullable or an empty string, then the external name of the service is implied to be the external name of the application.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


