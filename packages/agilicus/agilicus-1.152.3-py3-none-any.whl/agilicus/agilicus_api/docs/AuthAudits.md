# AuthAudits

An audit record containing authentication related actions. Each stage of the authentication pipeline emits a record indicating what is going on: who is performing the action, what they are trying to log in to, whether they succeeded, etc. Use this to determine who accessed the system and when, as well as help with troubleshooting authentication issues. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | The system-local id of the user performing the action. | [optional] 
**upstream_user_id** | **str** | The id of the user in the upstream system, if available. | [optional] 
**org_id** | **str** | The id of the organisation of the issuer against which the user is authenticating.  | [optional] 
**org_name** | **str** | The name of the organisation of the issuer against which the user is authenticating.  | [optional] 
**time** | **datetime** | the time at which the record was generated. | [optional] 
**event** | **str** | The event which generated the record. The meaning of the event depends on the stage where it occured.  | [optional] 
**source_ip** | **str** | The IP address of the host initiating the action | [optional] 
**token_id** | **str** | The id of the token issued or reissued as part of the authentication. | [optional] 
**trace_id** | **str** | A correlation ID associated with requests related to this event | [optional] 
**session** | **str** | The session associated with tokens related to this event. This can be used to tie the actions undertaking by requests bearing tokens with the same session back to the authentication events which created the tokens.  | [optional] 
**issuer** | **str** | The issuer the user logged in to. | [optional] 
**client_id** | **str** | The client id of the web application, client, etc. that the user is logging in with. Note that this is not the id of the &#x60;IssuerClient&#x60;, but rather the id presented to the authentication system to identify that client. This corresponds to &#x60;name&#x60; in the &#x60;IssuerClient&#x60;.  | [optional] 
**application_name** | **str** | The name of the application within the system the user is logging in to. | [optional] 
**login_org_id** | **str** | The id of the organisation that the user is logging in to. Note that this is disctinct from the &#x60;org_id&#x60; field, which is tied to the issuer. This id is tied to the application.  | [optional] 
**login_org_name** | **str** | The name of the organisation that the user is logging in to. This corresponds to &#x60;login_org_id&#x60;.  | [optional] 
**upstream_idp** | **str** | The name of the identity provider proving the identity of the user.  | [optional] 
**stage** | **str** | The stage of the login process. This identifies where in the pipeline the event was generated.  | [optional] 
**user_agent** | **str** | The user agent of the client used to perform the login.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


