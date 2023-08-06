# InterceptorConfig

The configuration associated with an interceptor.  The allow_list and disallow_list control which commands, processes or children processes will be handled by the interceptor. In absense of the allow_list and disallow_list, all processes are automatically intercepted. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allow_list** | [**[InterceptorCommand]**](InterceptorCommand.md) | A list of commands, when matched, will be handled by the interceptor | [optional] 
**disallow_list** | [**[InterceptorCommand]**](InterceptorCommand.md) | A list of commands, when matched, will not be handled by the interceptor | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


