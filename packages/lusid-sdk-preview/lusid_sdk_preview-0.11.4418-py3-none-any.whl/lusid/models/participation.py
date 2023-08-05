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


class Participation(object):
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
        'id': 'ResourceId',
        'placement_id': 'ResourceId',
        'order_id': 'ResourceId',
        'version': 'Version',
        'links': 'list[Link]'
    }

    attribute_map = {
        'id': 'id',
        'placement_id': 'placementId',
        'order_id': 'orderId',
        'version': 'version',
        'links': 'links'
    }

    required_map = {
        'id': 'required',
        'placement_id': 'required',
        'order_id': 'required',
        'version': 'optional',
        'links': 'optional'
    }

    def __init__(self, id=None, placement_id=None, order_id=None, version=None, links=None, local_vars_configuration=None):  # noqa: E501
        """Participation - a model defined in OpenAPI"
        
        :param id:  (required)
        :type id: lusid.ResourceId
        :param placement_id:  (required)
        :type placement_id: lusid.ResourceId
        :param order_id:  (required)
        :type order_id: lusid.ResourceId
        :param version: 
        :type version: lusid.Version
        :param links:  Collection of links.
        :type links: list[lusid.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._placement_id = None
        self._order_id = None
        self._version = None
        self._links = None
        self.discriminator = None

        self.id = id
        self.placement_id = placement_id
        self.order_id = order_id
        if version is not None:
            self.version = version
        self.links = links

    @property
    def id(self):
        """Gets the id of this Participation.  # noqa: E501


        :return: The id of this Participation.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Participation.


        :param id: The id of this Participation.  # noqa: E501
        :type id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def placement_id(self):
        """Gets the placement_id of this Participation.  # noqa: E501


        :return: The placement_id of this Participation.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._placement_id

    @placement_id.setter
    def placement_id(self, placement_id):
        """Sets the placement_id of this Participation.


        :param placement_id: The placement_id of this Participation.  # noqa: E501
        :type placement_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and placement_id is None:  # noqa: E501
            raise ValueError("Invalid value for `placement_id`, must not be `None`")  # noqa: E501

        self._placement_id = placement_id

    @property
    def order_id(self):
        """Gets the order_id of this Participation.  # noqa: E501


        :return: The order_id of this Participation.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this Participation.


        :param order_id: The order_id of this Participation.  # noqa: E501
        :type order_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and order_id is None:  # noqa: E501
            raise ValueError("Invalid value for `order_id`, must not be `None`")  # noqa: E501

        self._order_id = order_id

    @property
    def version(self):
        """Gets the version of this Participation.  # noqa: E501


        :return: The version of this Participation.  # noqa: E501
        :rtype: lusid.Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Participation.


        :param version: The version of this Participation.  # noqa: E501
        :type version: lusid.Version
        """

        self._version = version

    @property
    def links(self):
        """Gets the links of this Participation.  # noqa: E501

        Collection of links.  # noqa: E501

        :return: The links of this Participation.  # noqa: E501
        :rtype: list[lusid.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Participation.

        Collection of links.  # noqa: E501

        :param links: The links of this Participation.  # noqa: E501
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
        if not isinstance(other, Participation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Participation):
            return True

        return self.to_dict() != other.to_dict()
