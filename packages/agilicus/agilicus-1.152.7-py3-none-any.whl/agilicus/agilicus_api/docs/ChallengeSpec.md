# ChallengeSpec

The specification of an authentication challenge. Contains fields which control how the challenge is made. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | Unique identifier | [readonly] 
**challenge_type** | **str** | The type of challenge to issue. This controls how the user is informed of the challenge, as well as how the challenge can be satisfied. The follow types are supported:   - sms:  a &#x60;sms&#x60; challenge informs the user via text message of the challenge. The challenge can     be answered via the link provided in the text message. The user can deny the challenge via this     mechanism as well.   - web_push: a &#x60;web_push&#x60; challenge informs the user of the challenge on every device they have   registered via the web push (rfc8030) mechanism. If the user accepts via the link provided in   the web push, the challenge will be satisfied. The user can deny the challenge via this   mechanism as well.   - totp: a time-based one-time password challenge allows the user to enter the code from their registered   - webauthn: a challenge issued for a specific device the user has possession of. Either a yubikey, or a phone that has a Trusted Platform Module.   device and application. enum: [sms, web_push, totp, webauthn] example: web_push  | [optional] 
**challenge_types** | **[str]** | List of acceptable challenge types for this challenge request. The subsequent challenge answer must be one of these types. | [optional] 
**send_now** | **bool** | Whether to send the challenge now. If the challenge hasn&#39;t yet been set, setting this to true will send the challenge. If the challenge has been sent, changing this has no effect.  | [optional]  if omitted the server will use the default value of False
**timeout_seconds** | **int** | For how long the system will accept answers for the challenge. After this time, if the challenge is not in the &#x60;challenge_passed&#x60; state, it will transition into the &#x60;timed_out&#x60; state.  | [optional]  if omitted the server will use the default value of 600
**response_uri** | **str** | The base URI which the user should retrieve in order to answer the challenge. It is expected that this will be an HTTP endpoint serving &#x60;text/html&#x60; content. The final URI that the user should retrieve will be this value, extended with three form parameters that may be used to invoke the &#x60;answer&#x60; endpoint.   - challenge_answer: A string which is the answer code.   - challenge_uid: the id of the user being challenged.   - challenge_id: the id of the challenge. In the example, this would turn into something like: &#x60;https://auth.egov.city/mfa-answer?challenge_answer&#x3D;supersecret&amp;challenge_uid&#x3D;1234&amp;challenge_id&#x3D;5678&#x60;  | [optional] 
**origin** | **str** | The origin that is initiating the challenge. | [optional] 
**challenge_endpoints** | [**[ChallengeEndpoint]**](ChallengeEndpoint.md) | List of endpoint ids to challenge for this challenge request. At least one entry is required here when the challenge type includes webauthn. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


