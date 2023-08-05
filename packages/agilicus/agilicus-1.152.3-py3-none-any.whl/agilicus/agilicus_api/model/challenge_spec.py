"""
    Agilicus API

    Agilicus is API-first. Modern software is controlled by other software, is open, is available for you to use the way you want, securely, simply.  A rendered, online viewable and usable version of this specification is available at [api](https://www.agilicus.com/api). You may try the API inline directly in the web page. To do so, first obtain an Authentication Token (the simplest way is to install the Python SDK, and then run `agilicus-cli --issuer https://MYISSUER get-token`). You will need an org-id for most calls (and can obtain from `agilicus-cli --issuer https://MYISSUER list-orgs`). The `MYISSUER` will typically be `auth.MYDOMAIN`, and you will see it as you sign-in to the administrative UI.  This API releases on Bearer-Token authentication. To obtain a valid bearer token you will need to Authenticate to an Issuer with OpenID Connect (a superset of OAUTH2).  Your \"issuer\" will look like https://auth.MYDOMAIN. For example, when you signed-up, if you said \"use my own domain name\" and assigned a CNAME of cloud.example.com, then your issuer would be https://auth.cloud.example.com.  If you selected \"use an Agilicus supplied domain name\", your issuer would look like https://auth.myorg.agilicus.cloud.  For test purposes you can use our [Python SDK](https://pypi.org/project/agilicus/) and run `agilicus-cli --issuer https://auth.MYDOMAIN get-token`.  This API may be used in any language runtime that supports OpenAPI 3.0, or, you may use our [Python SDK](https://pypi.org/project/agilicus/), our [Typescript SDK](https://www.npmjs.com/package/@agilicus/angular), or our [Golang SDK](https://git.agilicus.com/pub/sdk-go).  100% of the activities in our system our API-driven, from our web-admin, through our progressive web applications, to all internals: there is nothing that is not accessible.  For more information, see [developer resources](https://www.agilicus.com/developer).   # noqa: E501

    The version of the OpenAPI document: 2022.05.30
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from agilicus_api.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)
from ..model_utils import OpenApiModel
from agilicus_api.exceptions import ApiAttributeError


def lazy_import():
    from agilicus_api.model.challenge_endpoint import ChallengeEndpoint
    globals()['ChallengeEndpoint'] = ChallengeEndpoint


class ChallengeSpec(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
        ('challenge_types',): {
        },
        ('timeout_seconds',): {
            'inclusive_maximum': 3600,
            'inclusive_minimum': 1,
        },
        ('challenge_endpoints',): {
        },
    }

    @property
    def challenge_type(self):
       return self.get("challenge_type")

    @challenge_type.setter
    def challenge_type(self, new_value):
       self.challenge_type = new_value

    @property
    def challenge_types(self):
       return self.get("challenge_types")

    @challenge_types.setter
    def challenge_types(self, new_value):
       self.challenge_types = new_value

    @property
    def user_id(self):
       return self.get("user_id")

    @user_id.setter
    def user_id(self, new_value):
       self.user_id = new_value

    @property
    def send_now(self):
       return self.get("send_now")

    @send_now.setter
    def send_now(self, new_value):
       self.send_now = new_value

    @property
    def timeout_seconds(self):
       return self.get("timeout_seconds")

    @timeout_seconds.setter
    def timeout_seconds(self, new_value):
       self.timeout_seconds = new_value

    @property
    def response_uri(self):
       return self.get("response_uri")

    @response_uri.setter
    def response_uri(self, new_value):
       self.response_uri = new_value

    @property
    def origin(self):
       return self.get("origin")

    @origin.setter
    def origin(self, new_value):
       self.origin = new_value

    @property
    def challenge_endpoints(self):
       return self.get("challenge_endpoints")

    @challenge_endpoints.setter
    def challenge_endpoints(self, new_value):
       self.challenge_endpoints = new_value

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'user_id': (str,),  # noqa: E501
            'challenge_type': (str,),  # noqa: E501
            'challenge_types': ([str],),  # noqa: E501
            'send_now': (bool,),  # noqa: E501
            'timeout_seconds': (int,),  # noqa: E501
            'response_uri': (str,),  # noqa: E501
            'origin': (str,),  # noqa: E501
            'challenge_endpoints': ([ChallengeEndpoint],),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None



    attribute_map = {
        'user_id': 'user_id',  # noqa: E501
        'challenge_type': 'challenge_type',  # noqa: E501
        'challenge_types': 'challenge_types',  # noqa: E501
        'send_now': 'send_now',  # noqa: E501
        'timeout_seconds': 'timeout_seconds',  # noqa: E501
        'response_uri': 'response_uri',  # noqa: E501
        'origin': 'origin',  # noqa: E501
        'challenge_endpoints': 'challenge_endpoints',  # noqa: E501
    }

    read_only_vars = {
        'user_id',  # noqa: E501
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, user_id, *args, **kwargs):  # noqa: E501
        """ChallengeSpec - a model defined in OpenAPI

        Args:
            user_id (str): Unique identifier

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            challenge_type (str): The type of challenge to issue. This controls how the user is informed of the challenge, as well as how the challenge can be satisfied. The follow types are supported:   - sms:  a `sms` challenge informs the user via text message of the challenge. The challenge can     be answered via the link provided in the text message. The user can deny the challenge via this     mechanism as well.   - web_push: a `web_push` challenge informs the user of the challenge on every device they have   registered via the web push (rfc8030) mechanism. If the user accepts via the link provided in   the web push, the challenge will be satisfied. The user can deny the challenge via this   mechanism as well.   - totp: a time-based one-time password challenge allows the user to enter the code from their registered   - webauthn: a challenge issued for a specific device the user has possession of. Either a yubikey, or a phone that has a Trusted Platform Module.   device and application. enum: [sms, web_push, totp, webauthn] example: web_push . [optional]  # noqa: E501
            challenge_types ([str]): List of acceptable challenge types for this challenge request. The subsequent challenge answer must be one of these types.. [optional]  # noqa: E501
            send_now (bool): Whether to send the challenge now. If the challenge hasn't yet been set, setting this to true will send the challenge. If the challenge has been sent, changing this has no effect. . [optional] if omitted the server will use the default value of False  # noqa: E501
            timeout_seconds (int): For how long the system will accept answers for the challenge. After this time, if the challenge is not in the `challenge_passed` state, it will transition into the `timed_out` state. . [optional] if omitted the server will use the default value of 600  # noqa: E501
            response_uri (str): The base URI which the user should retrieve in order to answer the challenge. It is expected that this will be an HTTP endpoint serving `text/html` content. The final URI that the user should retrieve will be this value, extended with three form parameters that may be used to invoke the `answer` endpoint.   - challenge_answer: A string which is the answer code.   - challenge_uid: the id of the user being challenged.   - challenge_id: the id of the challenge. In the example, this would turn into something like: `https://auth.egov.city/mfa-answer?challenge_answer=supersecret&challenge_uid=1234&challenge_id=5678` . [optional]  # noqa: E501
            origin (str): The origin that is initiating the challenge.. [optional]  # noqa: E501
            challenge_endpoints ([ChallengeEndpoint]): List of endpoint ids to challenge for this challenge request. At least one entry is required here when the challenge type includes webauthn.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.user_id = user_id
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    def __python_set(val):
        return set(val)
 
    required_properties = __python_set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """ChallengeSpec - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            challenge_type (str): The type of challenge to issue. This controls how the user is informed of the challenge, as well as how the challenge can be satisfied. The follow types are supported:   - sms:  a `sms` challenge informs the user via text message of the challenge. The challenge can     be answered via the link provided in the text message. The user can deny the challenge via this     mechanism as well.   - web_push: a `web_push` challenge informs the user of the challenge on every device they have   registered via the web push (rfc8030) mechanism. If the user accepts via the link provided in   the web push, the challenge will be satisfied. The user can deny the challenge via this   mechanism as well.   - totp: a time-based one-time password challenge allows the user to enter the code from their registered   - webauthn: a challenge issued for a specific device the user has possession of. Either a yubikey, or a phone that has a Trusted Platform Module.   device and application. enum: [sms, web_push, totp, webauthn] example: web_push . [optional]  # noqa: E501
            challenge_types ([str]): List of acceptable challenge types for this challenge request. The subsequent challenge answer must be one of these types.. [optional]  # noqa: E501
            send_now (bool): Whether to send the challenge now. If the challenge hasn't yet been set, setting this to true will send the challenge. If the challenge has been sent, changing this has no effect. . [optional] if omitted the server will use the default value of False  # noqa: E501
            timeout_seconds (int): For how long the system will accept answers for the challenge. After this time, if the challenge is not in the `challenge_passed` state, it will transition into the `timed_out` state. . [optional] if omitted the server will use the default value of 600  # noqa: E501
            response_uri (str): The base URI which the user should retrieve in order to answer the challenge. It is expected that this will be an HTTP endpoint serving `text/html` content. The final URI that the user should retrieve will be this value, extended with three form parameters that may be used to invoke the `answer` endpoint.   - challenge_answer: A string which is the answer code.   - challenge_uid: the id of the user being challenged.   - challenge_id: the id of the challenge. In the example, this would turn into something like: `https://auth.egov.city/mfa-answer?challenge_answer=supersecret&challenge_uid=1234&challenge_id=5678` . [optional]  # noqa: E501
            origin (str): The origin that is initiating the challenge.. [optional]  # noqa: E501
            challenge_endpoints ([ChallengeEndpoint]): List of endpoint ids to challenge for this challenge request. At least one entry is required here when the challenge type includes webauthn.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")

