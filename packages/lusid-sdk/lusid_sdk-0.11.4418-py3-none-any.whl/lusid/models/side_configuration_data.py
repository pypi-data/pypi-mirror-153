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


class SideConfigurationData(object):
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
        'side': 'str',
        'security': 'str',
        'currency': 'str',
        'rate': 'str',
        'units': 'str',
        'amount': 'str',
        'links': 'list[Link]'
    }

    attribute_map = {
        'side': 'side',
        'security': 'security',
        'currency': 'currency',
        'rate': 'rate',
        'units': 'units',
        'amount': 'amount',
        'links': 'links'
    }

    required_map = {
        'side': 'required',
        'security': 'required',
        'currency': 'required',
        'rate': 'required',
        'units': 'required',
        'amount': 'required',
        'links': 'optional'
    }

    def __init__(self, side=None, security=None, currency=None, rate=None, units=None, amount=None, links=None, local_vars_configuration=None):  # noqa: E501
        """SideConfigurationData - a model defined in OpenAPI"
        
        :param side:  The side's label. (required)
        :type side: str
        :param security:  The security, or instrument. (required)
        :type security: str
        :param currency:  The currency. (required)
        :type currency: str
        :param rate:  The rate. (required)
        :type rate: str
        :param units:  The units. (required)
        :type units: str
        :param amount:  The amount. (required)
        :type amount: str
        :param links:  Collection of links.
        :type links: list[lusid.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._side = None
        self._security = None
        self._currency = None
        self._rate = None
        self._units = None
        self._amount = None
        self._links = None
        self.discriminator = None

        self.side = side
        self.security = security
        self.currency = currency
        self.rate = rate
        self.units = units
        self.amount = amount
        self.links = links

    @property
    def side(self):
        """Gets the side of this SideConfigurationData.  # noqa: E501

        The side's label.  # noqa: E501

        :return: The side of this SideConfigurationData.  # noqa: E501
        :rtype: str
        """
        return self._side

    @side.setter
    def side(self, side):
        """Sets the side of this SideConfigurationData.

        The side's label.  # noqa: E501

        :param side: The side of this SideConfigurationData.  # noqa: E501
        :type side: str
        """
        if self.local_vars_configuration.client_side_validation and side is None:  # noqa: E501
            raise ValueError("Invalid value for `side`, must not be `None`")  # noqa: E501

        self._side = side

    @property
    def security(self):
        """Gets the security of this SideConfigurationData.  # noqa: E501

        The security, or instrument.  # noqa: E501

        :return: The security of this SideConfigurationData.  # noqa: E501
        :rtype: str
        """
        return self._security

    @security.setter
    def security(self, security):
        """Sets the security of this SideConfigurationData.

        The security, or instrument.  # noqa: E501

        :param security: The security of this SideConfigurationData.  # noqa: E501
        :type security: str
        """
        if self.local_vars_configuration.client_side_validation and security is None:  # noqa: E501
            raise ValueError("Invalid value for `security`, must not be `None`")  # noqa: E501

        self._security = security

    @property
    def currency(self):
        """Gets the currency of this SideConfigurationData.  # noqa: E501

        The currency.  # noqa: E501

        :return: The currency of this SideConfigurationData.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this SideConfigurationData.

        The currency.  # noqa: E501

        :param currency: The currency of this SideConfigurationData.  # noqa: E501
        :type currency: str
        """
        if self.local_vars_configuration.client_side_validation and currency is None:  # noqa: E501
            raise ValueError("Invalid value for `currency`, must not be `None`")  # noqa: E501

        self._currency = currency

    @property
    def rate(self):
        """Gets the rate of this SideConfigurationData.  # noqa: E501

        The rate.  # noqa: E501

        :return: The rate of this SideConfigurationData.  # noqa: E501
        :rtype: str
        """
        return self._rate

    @rate.setter
    def rate(self, rate):
        """Sets the rate of this SideConfigurationData.

        The rate.  # noqa: E501

        :param rate: The rate of this SideConfigurationData.  # noqa: E501
        :type rate: str
        """
        if self.local_vars_configuration.client_side_validation and rate is None:  # noqa: E501
            raise ValueError("Invalid value for `rate`, must not be `None`")  # noqa: E501

        self._rate = rate

    @property
    def units(self):
        """Gets the units of this SideConfigurationData.  # noqa: E501

        The units.  # noqa: E501

        :return: The units of this SideConfigurationData.  # noqa: E501
        :rtype: str
        """
        return self._units

    @units.setter
    def units(self, units):
        """Sets the units of this SideConfigurationData.

        The units.  # noqa: E501

        :param units: The units of this SideConfigurationData.  # noqa: E501
        :type units: str
        """
        if self.local_vars_configuration.client_side_validation and units is None:  # noqa: E501
            raise ValueError("Invalid value for `units`, must not be `None`")  # noqa: E501

        self._units = units

    @property
    def amount(self):
        """Gets the amount of this SideConfigurationData.  # noqa: E501

        The amount.  # noqa: E501

        :return: The amount of this SideConfigurationData.  # noqa: E501
        :rtype: str
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this SideConfigurationData.

        The amount.  # noqa: E501

        :param amount: The amount of this SideConfigurationData.  # noqa: E501
        :type amount: str
        """
        if self.local_vars_configuration.client_side_validation and amount is None:  # noqa: E501
            raise ValueError("Invalid value for `amount`, must not be `None`")  # noqa: E501

        self._amount = amount

    @property
    def links(self):
        """Gets the links of this SideConfigurationData.  # noqa: E501

        Collection of links.  # noqa: E501

        :return: The links of this SideConfigurationData.  # noqa: E501
        :rtype: list[lusid.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this SideConfigurationData.

        Collection of links.  # noqa: E501

        :param links: The links of this SideConfigurationData.  # noqa: E501
        :type links: list[lusid.Link]
        """

        self._links = links

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
        if not isinstance(other, SideConfigurationData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SideConfigurationData):
            return True

        return self.to_dict() != other.to_dict()
