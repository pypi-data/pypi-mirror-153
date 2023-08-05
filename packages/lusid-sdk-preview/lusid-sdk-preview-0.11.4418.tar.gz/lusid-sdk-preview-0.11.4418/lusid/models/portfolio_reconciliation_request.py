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


class PortfolioReconciliationRequest(object):
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
        'portfolio_id': 'ResourceId',
        'effective_at': 'str',
        'as_at': 'datetime'
    }

    attribute_map = {
        'portfolio_id': 'portfolioId',
        'effective_at': 'effectiveAt',
        'as_at': 'asAt'
    }

    required_map = {
        'portfolio_id': 'required',
        'effective_at': 'required',
        'as_at': 'optional'
    }

    def __init__(self, portfolio_id=None, effective_at=None, as_at=None, local_vars_configuration=None):  # noqa: E501
        """PortfolioReconciliationRequest - a model defined in OpenAPI"
        
        :param portfolio_id:  (required)
        :type portfolio_id: lusid.ResourceId
        :param effective_at:  The effective date of the portfolio (required)
        :type effective_at: str
        :param as_at:  Optional. The AsAt date of the portfolio
        :type as_at: datetime

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._portfolio_id = None
        self._effective_at = None
        self._as_at = None
        self.discriminator = None

        self.portfolio_id = portfolio_id
        self.effective_at = effective_at
        self.as_at = as_at

    @property
    def portfolio_id(self):
        """Gets the portfolio_id of this PortfolioReconciliationRequest.  # noqa: E501


        :return: The portfolio_id of this PortfolioReconciliationRequest.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, portfolio_id):
        """Sets the portfolio_id of this PortfolioReconciliationRequest.


        :param portfolio_id: The portfolio_id of this PortfolioReconciliationRequest.  # noqa: E501
        :type portfolio_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and portfolio_id is None:  # noqa: E501
            raise ValueError("Invalid value for `portfolio_id`, must not be `None`")  # noqa: E501

        self._portfolio_id = portfolio_id

    @property
    def effective_at(self):
        """Gets the effective_at of this PortfolioReconciliationRequest.  # noqa: E501

        The effective date of the portfolio  # noqa: E501

        :return: The effective_at of this PortfolioReconciliationRequest.  # noqa: E501
        :rtype: str
        """
        return self._effective_at

    @effective_at.setter
    def effective_at(self, effective_at):
        """Sets the effective_at of this PortfolioReconciliationRequest.

        The effective date of the portfolio  # noqa: E501

        :param effective_at: The effective_at of this PortfolioReconciliationRequest.  # noqa: E501
        :type effective_at: str
        """
        if self.local_vars_configuration.client_side_validation and effective_at is None:  # noqa: E501
            raise ValueError("Invalid value for `effective_at`, must not be `None`")  # noqa: E501

        self._effective_at = effective_at

    @property
    def as_at(self):
        """Gets the as_at of this PortfolioReconciliationRequest.  # noqa: E501

        Optional. The AsAt date of the portfolio  # noqa: E501

        :return: The as_at of this PortfolioReconciliationRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._as_at

    @as_at.setter
    def as_at(self, as_at):
        """Sets the as_at of this PortfolioReconciliationRequest.

        Optional. The AsAt date of the portfolio  # noqa: E501

        :param as_at: The as_at of this PortfolioReconciliationRequest.  # noqa: E501
        :type as_at: datetime
        """

        self._as_at = as_at

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
        if not isinstance(other, PortfolioReconciliationRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PortfolioReconciliationRequest):
            return True

        return self.to_dict() != other.to_dict()
