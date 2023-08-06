# BillingAccountStatus

Object describing the spec of a Billing Account

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**orgs** | [**[Organisation]**](Organisation.md) | the list of organisations that are connected to this billing account.  | [optional] 
**subscriptions** | [**[BillingSubscription]**](BillingSubscription.md) | The subscriptions associated with this billing account.  | [optional] 
**customer** | [**BillingCustomer**](BillingCustomer.md) |  | [optional] 
**products** | [**[BillingProduct]**](BillingProduct.md) | The products associated with this billing account.  | [optional] 
**product** | [**Product**](Product.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


