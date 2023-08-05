# WhoamiResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** | access token | [optional] 
**orgs** | [**[Organisation]**](Organisation.md) | list of orgs user belongs to | [optional] [readonly] 
**member_of** | [**[UserIdentity]**](UserIdentity.md) | List of groups that the user is a member of | [optional] 
**id** | **str** | Unique identifier | [optional] [readonly] 
**external_id** | **str, none_type** | External unique identifier | [optional] 
**enabled** | **bool** | Enable/Disable a user | [optional] 
**status** | [**UserStatusEnum**](UserStatusEnum.md) |  | [optional] 
**first_name** | **str** | User&#39;s first name | [optional] 
**last_name** | **str** | User&#39;s last name | [optional] 
**email** | [**Email**](Email.md) |  | [optional] 
**provider** | **str, none_type** | Upstream IdP name | [optional] 
**roles** | [**Roles**](Roles.md) |  | [optional] 
**org_id** | **str** | Unique identifier | [optional] 
**type** | **str** | Type of user | [optional] [readonly] 
**created** | **datetime** | Creation time | [optional] [readonly] 
**updated** | **datetime** | Update time | [optional] [readonly] 
**auto_created** | **bool** | Whether the user was automatically created as part of another process such as logging in. On creation, this flag being true serves to trigger any behaviour tied to automatically created users, such as addition to special groups. On read, it can serve to indicate whether the user was automatically created. On update it will ensure that the automatically triggered behaviour still holds true.  | [optional]  if omitted the server will use the default value of False
**upstream_user_identities** | [**[UpstreamUserIdentity]**](UpstreamUserIdentity.md) | The upstream identities this user can use to log in to the system. When a user logs in, their identity in this system will be determined by matching against this list. Note that this implies that entries in this list are globally unique.  | [optional] [readonly] 
**cascade** | **bool** | Whether the user will be added to sub organisations automatically. When set for a user that is a member of a particular organisation, subsequent creations of sub organisations will add this user to that suborgansation.  | [optional]  if omitted the server will use the default value of False
**configured_attributes** | [**UserAttributes**](UserAttributes.md) |  | [optional] 
**attributes** | [**[UserAttribute]**](UserAttribute.md) | The live attributes of the user, as determined from all sources of attributes. A user&#39;s attributes flow from all of their upstream_user_identities as well as the &#x60;configured_attributes&#x60; field. Attributes are merged by name. If two sources of attributes have an attribute with the same name, that attribute will be merged. For cases where a merge is not possible -- e.g. two attributes with different types -- the oldest source of identity will be used. The &#x60;configured_attributes&#x60; field is always considered the oldest, so it has priority. Further, the resulting items will be sorted in ascending order of name.  For example, considering a user with following two sources of attributes:  &#x60;&#x60;&#x60; older_upstream:   - name: manager     value: best-manager   - name: groups     value: [\&quot;A\&quot;, \&quot;B\&quot;] newer_upstream:   - name: manager     value: other-manager   - name: groups     value: [\&quot;C\&quot;]   - name: age     value 32 &#x60;&#x60;&#x60;  The resulting attributes will be:  &#x60;&#x60;&#x60; attributes:   - name: age     value 32   - name: groups     value: [\&quot;A\&quot;, \&quot;B\&quot;, \&quot;C\&quot;]   - name: manager     value: best-manager &#x60;&#x60;&#x60;  | [optional] [readonly] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


