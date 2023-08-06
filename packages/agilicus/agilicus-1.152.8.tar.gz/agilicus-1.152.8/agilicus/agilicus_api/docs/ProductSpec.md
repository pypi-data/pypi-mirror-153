# ProductSpec

The specification for a Product.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The product&#39;s name, meant to be displayable to the customer. | 
**dev_mode** | **bool** | Product is in dev mode, used for connecting to non-live backend billing API.  | [optional] 
**billing_product_prices** | [**[BillingProductPrice]**](BillingProductPrice.md) | A list of billing product price ids that are contained in this Product | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


