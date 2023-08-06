# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose">
#   Copyright (c) 2018 Aspose.Slides for Cloud
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

import pprint
import re  # noqa: F401

import six

from asposeslidescloud.models.resource_base import ResourceBase

class Placeholder(ResourceBase):


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'self_uri': 'ResourceUri',
        'alternate_links': 'list[ResourceUri]',
        'index': 'int',
        'orientation': 'str',
        'size': 'str',
        'type': 'str',
        'shape': 'ResourceUri'
    }

    attribute_map = {
        'self_uri': 'selfUri',
        'alternate_links': 'alternateLinks',
        'index': 'index',
        'orientation': 'orientation',
        'size': 'size',
        'type': 'type',
        'shape': 'shape'
    }

    type_determiners = {
    }

    def __init__(self, self_uri=None, alternate_links=None, index=None, orientation=None, size=None, type=None, shape=None):  # noqa: E501
        """Placeholder - a model defined in Swagger"""  # noqa: E501
        super(Placeholder, self).__init__(self_uri, alternate_links)

        self._index = None
        self._orientation = None
        self._size = None
        self._type = None
        self._shape = None

        self.index = index
        self.orientation = orientation
        self.size = size
        self.type = type
        if shape is not None:
            self.shape = shape

    @property
    def index(self):
        """Gets the index of this Placeholder.  # noqa: E501

        Index.  # noqa: E501

        :return: The index of this Placeholder.  # noqa: E501
        :rtype: int
        """
        return self._index

    @index.setter
    def index(self, index):
        """Sets the index of this Placeholder.

        Index.  # noqa: E501

        :param index: The index of this Placeholder.  # noqa: E501
        :type: int
        """
        self._index = index

    @property
    def orientation(self):
        """Gets the orientation of this Placeholder.  # noqa: E501

        Orientation.  # noqa: E501

        :return: The orientation of this Placeholder.  # noqa: E501
        :rtype: str
        """
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        """Sets the orientation of this Placeholder.

        Orientation.  # noqa: E501

        :param orientation: The orientation of this Placeholder.  # noqa: E501
        :type: str
        """
        if orientation is not None:
            allowed_values = ["Horizontal", "Vertical"]  # noqa: E501
            if orientation.isdigit():
                int_orientation = int(orientation)
                if int_orientation < 0 or int_orientation >= len(allowed_values):
                    raise ValueError(
                        "Invalid value for `orientation` ({0}), must be one of {1}"  # noqa: E501
                        .format(orientation, allowed_values)
                    )
                self._orientation = allowed_values[int_orientation]
                return
            if orientation not in allowed_values:
                raise ValueError(
                    "Invalid value for `orientation` ({0}), must be one of {1}"  # noqa: E501
                    .format(orientation, allowed_values)
                )
        self._orientation = orientation

    @property
    def size(self):
        """Gets the size of this Placeholder.  # noqa: E501

        Size.  # noqa: E501

        :return: The size of this Placeholder.  # noqa: E501
        :rtype: str
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this Placeholder.

        Size.  # noqa: E501

        :param size: The size of this Placeholder.  # noqa: E501
        :type: str
        """
        if size is not None:
            allowed_values = ["Full", "Half", "Quarter"]  # noqa: E501
            if size.isdigit():
                int_size = int(size)
                if int_size < 0 or int_size >= len(allowed_values):
                    raise ValueError(
                        "Invalid value for `size` ({0}), must be one of {1}"  # noqa: E501
                        .format(size, allowed_values)
                    )
                self._size = allowed_values[int_size]
                return
            if size not in allowed_values:
                raise ValueError(
                    "Invalid value for `size` ({0}), must be one of {1}"  # noqa: E501
                    .format(size, allowed_values)
                )
        self._size = size

    @property
    def type(self):
        """Gets the type of this Placeholder.  # noqa: E501

        Placeholder type.  # noqa: E501

        :return: The type of this Placeholder.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Placeholder.

        Placeholder type.  # noqa: E501

        :param type: The type of this Placeholder.  # noqa: E501
        :type: str
        """
        if type is not None:
            allowed_values = ["Title", "Body", "CenteredTitle", "Subtitle", "DateAndTime", "SlideNumber", "Footer", "Header", "Object", "Chart", "Table", "ClipArt", "Diagram", "Media", "SlideImage", "Picture"]  # noqa: E501
            if type.isdigit():
                int_type = int(type)
                if int_type < 0 or int_type >= len(allowed_values):
                    raise ValueError(
                        "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                        .format(type, allowed_values)
                    )
                self._type = allowed_values[int_type]
                return
            if type not in allowed_values:
                raise ValueError(
                    "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                    .format(type, allowed_values)
                )
        self._type = type

    @property
    def shape(self):
        """Gets the shape of this Placeholder.  # noqa: E501

        Shape link.  # noqa: E501

        :return: The shape of this Placeholder.  # noqa: E501
        :rtype: ResourceUri
        """
        return self._shape

    @shape.setter
    def shape(self, shape):
        """Sets the shape of this Placeholder.

        Shape link.  # noqa: E501

        :param shape: The shape of this Placeholder.  # noqa: E501
        :type: ResourceUri
        """
        self._shape = shape

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Placeholder):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
