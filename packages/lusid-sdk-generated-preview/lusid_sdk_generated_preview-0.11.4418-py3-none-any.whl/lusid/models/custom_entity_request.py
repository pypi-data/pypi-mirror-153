# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.4418
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class CustomEntityRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'display_name': 'str',
        'description': 'str',
        'identifiers': 'list[CustomEntityId]',
        'fields': 'list[CustomEntityField]'
    }

    attribute_map = {
        'display_name': 'displayName',
        'description': 'description',
        'identifiers': 'identifiers',
        'fields': 'fields'
    }

    required_map = {
        'display_name': 'required',
        'description': 'required',
        'identifiers': 'required',
        'fields': 'optional'
    }

    def __init__(self, display_name=None, description=None, identifiers=None, fields=None, local_vars_configuration=None):  # noqa: E501
        """CustomEntityRequest - a model defined in OpenAPI"
        
        :param display_name:  A display label for the custom entity. (required)
        :type display_name: str
        :param description:  A description of the custom entity. (required)
        :type description: str
        :param identifiers:  The identifiers the custom entity will be upserted with. (required)
        :type identifiers: list[lusid.CustomEntityId]
        :param fields:  The fields that decorate the custom entity.
        :type fields: list[lusid.CustomEntityField]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._display_name = None
        self._description = None
        self._identifiers = None
        self._fields = None
        self.discriminator = None

        self.display_name = display_name
        self.description = description
        self.identifiers = identifiers
        self.fields = fields

    @property
    def display_name(self):
        """Gets the display_name of this CustomEntityRequest.  # noqa: E501

        A display label for the custom entity.  # noqa: E501

        :return: The display_name of this CustomEntityRequest.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this CustomEntityRequest.

        A display label for the custom entity.  # noqa: E501

        :param display_name: The display_name of this CustomEntityRequest.  # noqa: E501
        :type display_name: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501

        self._display_name = display_name

    @property
    def description(self):
        """Gets the description of this CustomEntityRequest.  # noqa: E501

        A description of the custom entity.  # noqa: E501

        :return: The description of this CustomEntityRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CustomEntityRequest.

        A description of the custom entity.  # noqa: E501

        :param description: The description of this CustomEntityRequest.  # noqa: E501
        :type description: str
        """
        if self.local_vars_configuration.client_side_validation and description is None:  # noqa: E501
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def identifiers(self):
        """Gets the identifiers of this CustomEntityRequest.  # noqa: E501

        The identifiers the custom entity will be upserted with.  # noqa: E501

        :return: The identifiers of this CustomEntityRequest.  # noqa: E501
        :rtype: list[lusid.CustomEntityId]
        """
        return self._identifiers

    @identifiers.setter
    def identifiers(self, identifiers):
        """Sets the identifiers of this CustomEntityRequest.

        The identifiers the custom entity will be upserted with.  # noqa: E501

        :param identifiers: The identifiers of this CustomEntityRequest.  # noqa: E501
        :type identifiers: list[lusid.CustomEntityId]
        """
        if self.local_vars_configuration.client_side_validation and identifiers is None:  # noqa: E501
            raise ValueError("Invalid value for `identifiers`, must not be `None`")  # noqa: E501

        self._identifiers = identifiers

    @property
    def fields(self):
        """Gets the fields of this CustomEntityRequest.  # noqa: E501

        The fields that decorate the custom entity.  # noqa: E501

        :return: The fields of this CustomEntityRequest.  # noqa: E501
        :rtype: list[lusid.CustomEntityField]
        """
        return self._fields

    @fields.setter
    def fields(self, fields):
        """Sets the fields of this CustomEntityRequest.

        The fields that decorate the custom entity.  # noqa: E501

        :param fields: The fields of this CustomEntityRequest.  # noqa: E501
        :type fields: list[lusid.CustomEntityField]
        """

        self._fields = fields

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CustomEntityRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CustomEntityRequest):
            return True

        return self.to_dict() != other.to_dict()
