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


class UpsertCorporateActionRequest(object):
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
        'corporate_action_code': 'str',
        'description': 'str',
        'announcement_date': 'datetime',
        'ex_date': 'datetime',
        'record_date': 'datetime',
        'payment_date': 'datetime',
        'transitions': 'list[CorporateActionTransitionRequest]'
    }

    attribute_map = {
        'corporate_action_code': 'corporateActionCode',
        'description': 'description',
        'announcement_date': 'announcementDate',
        'ex_date': 'exDate',
        'record_date': 'recordDate',
        'payment_date': 'paymentDate',
        'transitions': 'transitions'
    }

    required_map = {
        'corporate_action_code': 'required',
        'description': 'optional',
        'announcement_date': 'required',
        'ex_date': 'required',
        'record_date': 'required',
        'payment_date': 'required',
        'transitions': 'required'
    }

    def __init__(self, corporate_action_code=None, description=None, announcement_date=None, ex_date=None, record_date=None, payment_date=None, transitions=None, local_vars_configuration=None):  # noqa: E501
        """UpsertCorporateActionRequest - a model defined in OpenAPI"
        
        :param corporate_action_code:  The unique identifier of this corporate action (required)
        :type corporate_action_code: str
        :param description:  The description of the corporate action.
        :type description: str
        :param announcement_date:  The announcement date of the corporate action (required)
        :type announcement_date: datetime
        :param ex_date:  The ex date of the corporate action (required)
        :type ex_date: datetime
        :param record_date:  The record date of the corporate action (required)
        :type record_date: datetime
        :param payment_date:  The payment date of the corporate action (required)
        :type payment_date: datetime
        :param transitions:  The transitions that result from this corporate action (required)
        :type transitions: list[lusid.CorporateActionTransitionRequest]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._corporate_action_code = None
        self._description = None
        self._announcement_date = None
        self._ex_date = None
        self._record_date = None
        self._payment_date = None
        self._transitions = None
        self.discriminator = None

        self.corporate_action_code = corporate_action_code
        self.description = description
        self.announcement_date = announcement_date
        self.ex_date = ex_date
        self.record_date = record_date
        self.payment_date = payment_date
        self.transitions = transitions

    @property
    def corporate_action_code(self):
        """Gets the corporate_action_code of this UpsertCorporateActionRequest.  # noqa: E501

        The unique identifier of this corporate action  # noqa: E501

        :return: The corporate_action_code of this UpsertCorporateActionRequest.  # noqa: E501
        :rtype: str
        """
        return self._corporate_action_code

    @corporate_action_code.setter
    def corporate_action_code(self, corporate_action_code):
        """Sets the corporate_action_code of this UpsertCorporateActionRequest.

        The unique identifier of this corporate action  # noqa: E501

        :param corporate_action_code: The corporate_action_code of this UpsertCorporateActionRequest.  # noqa: E501
        :type corporate_action_code: str
        """
        if self.local_vars_configuration.client_side_validation and corporate_action_code is None:  # noqa: E501
            raise ValueError("Invalid value for `corporate_action_code`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                corporate_action_code is not None and len(corporate_action_code) > 64):
            raise ValueError("Invalid value for `corporate_action_code`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                corporate_action_code is not None and len(corporate_action_code) < 1):
            raise ValueError("Invalid value for `corporate_action_code`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                corporate_action_code is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', corporate_action_code)):  # noqa: E501
            raise ValueError(r"Invalid value for `corporate_action_code`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._corporate_action_code = corporate_action_code

    @property
    def description(self):
        """Gets the description of this UpsertCorporateActionRequest.  # noqa: E501

        The description of the corporate action.  # noqa: E501

        :return: The description of this UpsertCorporateActionRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpsertCorporateActionRequest.

        The description of the corporate action.  # noqa: E501

        :param description: The description of this UpsertCorporateActionRequest.  # noqa: E501
        :type description: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 1024):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 0):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and not re.search(r'^[\s\S]*$', description)):  # noqa: E501
            raise ValueError(r"Invalid value for `description`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._description = description

    @property
    def announcement_date(self):
        """Gets the announcement_date of this UpsertCorporateActionRequest.  # noqa: E501

        The announcement date of the corporate action  # noqa: E501

        :return: The announcement_date of this UpsertCorporateActionRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._announcement_date

    @announcement_date.setter
    def announcement_date(self, announcement_date):
        """Sets the announcement_date of this UpsertCorporateActionRequest.

        The announcement date of the corporate action  # noqa: E501

        :param announcement_date: The announcement_date of this UpsertCorporateActionRequest.  # noqa: E501
        :type announcement_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and announcement_date is None:  # noqa: E501
            raise ValueError("Invalid value for `announcement_date`, must not be `None`")  # noqa: E501

        self._announcement_date = announcement_date

    @property
    def ex_date(self):
        """Gets the ex_date of this UpsertCorporateActionRequest.  # noqa: E501

        The ex date of the corporate action  # noqa: E501

        :return: The ex_date of this UpsertCorporateActionRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._ex_date

    @ex_date.setter
    def ex_date(self, ex_date):
        """Sets the ex_date of this UpsertCorporateActionRequest.

        The ex date of the corporate action  # noqa: E501

        :param ex_date: The ex_date of this UpsertCorporateActionRequest.  # noqa: E501
        :type ex_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and ex_date is None:  # noqa: E501
            raise ValueError("Invalid value for `ex_date`, must not be `None`")  # noqa: E501

        self._ex_date = ex_date

    @property
    def record_date(self):
        """Gets the record_date of this UpsertCorporateActionRequest.  # noqa: E501

        The record date of the corporate action  # noqa: E501

        :return: The record_date of this UpsertCorporateActionRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._record_date

    @record_date.setter
    def record_date(self, record_date):
        """Sets the record_date of this UpsertCorporateActionRequest.

        The record date of the corporate action  # noqa: E501

        :param record_date: The record_date of this UpsertCorporateActionRequest.  # noqa: E501
        :type record_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and record_date is None:  # noqa: E501
            raise ValueError("Invalid value for `record_date`, must not be `None`")  # noqa: E501

        self._record_date = record_date

    @property
    def payment_date(self):
        """Gets the payment_date of this UpsertCorporateActionRequest.  # noqa: E501

        The payment date of the corporate action  # noqa: E501

        :return: The payment_date of this UpsertCorporateActionRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._payment_date

    @payment_date.setter
    def payment_date(self, payment_date):
        """Sets the payment_date of this UpsertCorporateActionRequest.

        The payment date of the corporate action  # noqa: E501

        :param payment_date: The payment_date of this UpsertCorporateActionRequest.  # noqa: E501
        :type payment_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and payment_date is None:  # noqa: E501
            raise ValueError("Invalid value for `payment_date`, must not be `None`")  # noqa: E501

        self._payment_date = payment_date

    @property
    def transitions(self):
        """Gets the transitions of this UpsertCorporateActionRequest.  # noqa: E501

        The transitions that result from this corporate action  # noqa: E501

        :return: The transitions of this UpsertCorporateActionRequest.  # noqa: E501
        :rtype: list[lusid.CorporateActionTransitionRequest]
        """
        return self._transitions

    @transitions.setter
    def transitions(self, transitions):
        """Sets the transitions of this UpsertCorporateActionRequest.

        The transitions that result from this corporate action  # noqa: E501

        :param transitions: The transitions of this UpsertCorporateActionRequest.  # noqa: E501
        :type transitions: list[lusid.CorporateActionTransitionRequest]
        """
        if self.local_vars_configuration.client_side_validation and transitions is None:  # noqa: E501
            raise ValueError("Invalid value for `transitions`, must not be `None`")  # noqa: E501

        self._transitions = transitions

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
        if not isinstance(other, UpsertCorporateActionRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpsertCorporateActionRequest):
            return True

        return self.to_dict() != other.to_dict()
