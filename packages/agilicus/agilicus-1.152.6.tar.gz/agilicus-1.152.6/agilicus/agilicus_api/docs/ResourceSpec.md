# ResourceSpec

The configurable properties of a Resource. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The human readable name of the resource. Names are unique for a given resource type within an organisation.  | 
**resource_type** | **str** | The type of the resource. Resources of different types service different purposes, and have different behaviour. - An &#x60;application&#x60; provides high level functionality such as a website. Its fine-grained   permissions are configured on a per-application basis. It corresponds to an &#x60;Application&#x60;   resource. - A &#x60;fileshare&#x60; exposes a directory to the internet for file sharing purposes. Its permission model is fixed. It corresponds to a FileShareService resource. - An &#x60;application_service&#x60; exposes an IP based service to the internet. Its permission model is fixed. It corresponds to an ApplicationService resource. - A &#x60;desktop&#x60; securely exposes a Desktop for access using a protocol such as the Remote Desktop Protocol, via a   Desktop Gateway. - A &#x60;group&#x60; is a container that can hold resources. - A &#x60;launcher&#x60; exposes a Desktop Application Launcher that proxies its network   connectivity through Agilicus Resources  | 
**org_id** | **str** | The unique ID of the organisation which owns this Resource. | 
**name_slug** | [**K8sSlug**](K8sSlug.md) |  | [optional] 
**not_assignable_perm** | **bool** | Most resources can be assigned permission. However when a resource cannot be assigned a permission, this field is used (set to true), which notifies consumers of this API that the resource cannot be assigned a permission. This field defaults to false.  | [optional] 
**config** | [**ResourceConfig**](ResourceConfig.md) |  | [optional] 
**resource_members** | [**[ResourceMember]**](ResourceMember.md) | A list of resources that are contained or associated with this Resource. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


