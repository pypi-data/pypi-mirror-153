# AgentConnectorSpec

The specification of the Connector

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A descriptive name for the connector | 
**org_id** | **str** | Unique identifier | 
**name_slug** | [**K8sSlug**](K8sSlug.md) |  | [optional] 
**max_number_connections** | **int** | The maximum number of connections to maintain to the cluster when stable. Note that this value may be exceeded during times of reconfiguration. A value of zero means that the connector is effectively unused by this Secure Agent.  | [optional] 
**connection_uri** | **str** | Overrides the default URI used to connect to this connector. This can be used to point the Secure Agent somewhere other than the default.  | [optional] 
**service_account_required** | **bool** | If service_account_enabled field is set to true, a service account will be created. If service_account_enabled field is set to false, the service account will be deleted. If the service_account_enabled field is not set no action on the service account is taken.  | [optional] 
**local_authentication_enabled** | **bool** | Determines whether or not the agent will expose an endpoint for local authentication | [optional] 
**provisioning** | [**AgentConnectorSpecProvisioning**](AgentConnectorSpecProvisioning.md) |  | [optional] 
**routing** | [**AgentConnectorRouting**](AgentConnectorRouting.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


