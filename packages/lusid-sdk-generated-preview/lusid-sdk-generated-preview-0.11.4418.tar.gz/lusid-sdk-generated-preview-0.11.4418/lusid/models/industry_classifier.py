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


class IndustryClassifier(object):
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
        'classification_system_name': 'str',
        'classification_code': 'str'
    }

    attribute_map = {
        'classification_system_name': 'classificationSystemName',
        'classification_code': 'classificationCode'
    }

    required_map = {
        'classification_system_name': 'required',
        'classification_code': 'required'
    }

    def __init__(self, classification_system_name=None, classification_code=None, local_vars_configuration=None):  # noqa: E501
        """IndustryClassifier - a model defined in OpenAPI"
        
        :param classification_system_name:  The name of the classification system to which the classification code belongs (e.g. GICS). (required)
        :type classification_system_name: str
        :param classification_code:  The specific industry classification code assigned to the legal entity. (required)
        :type classification_code: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._classification_system_name = None
        self._classification_code = None
        self.discriminator = None

        self.classification_system_name = classification_system_name
        self.classification_code = classification_code

    @property
    def classification_system_name(self):
        """Gets the classification_system_name of this IndustryClassifier.  # noqa: E501

        The name of the classification system to which the classification code belongs (e.g. GICS).  # noqa: E501

        :return: The classification_system_name of this IndustryClassifier.  # noqa: E501
        :rtype: str
        """
        return self._classification_system_name

    @classification_system_name.setter
    def classification_system_name(self, classification_system_name):
        """Sets the classification_system_name of this IndustryClassifier.

        The name of the classification system to which the classification code belongs (e.g. GICS).  # noqa: E501

        :param classification_system_name: The classification_system_name of this IndustryClassifier.  # noqa: E501
        :type classification_system_name: str
        """
        if self.local_vars_configuration.client_side_validation and classification_system_name is None:  # noqa: E501
            raise ValueError("Invalid value for `classification_system_name`, must not be `None`")  # noqa: E501

        self._classification_system_name = classification_system_name

    @property
    def classification_code(self):
        """Gets the classification_code of this IndustryClassifier.  # noqa: E501

        The specific industry classification code assigned to the legal entity.  # noqa: E501

        :return: The classification_code of this IndustryClassifier.  # noqa: E501
        :rtype: str
        """
        return self._classification_code

    @classification_code.setter
    def classification_code(self, classification_code):
        """Sets the classification_code of this IndustryClassifier.

        The specific industry classification code assigned to the legal entity.  # noqa: E501

        :param classification_code: The classification_code of this IndustryClassifier.  # noqa: E501
        :type classification_code: str
        """
        if self.local_vars_configuration.client_side_validation and classification_code is None:  # noqa: E501
            raise ValueError("Invalid value for `classification_code`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                classification_code is not None and len(classification_code) > 64):
            raise ValueError("Invalid value for `classification_code`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                classification_code is not None and len(classification_code) < 1):
            raise ValueError("Invalid value for `classification_code`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                classification_code is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', classification_code)):  # noqa: E501
            raise ValueError(r"Invalid value for `classification_code`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._classification_code = classification_code

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
        if not isinstance(other, IndustryClassifier):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, IndustryClassifier):
            return True

        return self.to_dict() != other.to_dict()
