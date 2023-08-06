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


class NormalViewRestoredProperties(object):


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'auto_adjust': 'bool',
        'dimension_size': 'float'
    }

    attribute_map = {
        'auto_adjust': 'autoAdjust',
        'dimension_size': 'dimensionSize'
    }

    type_determiners = {
    }

    def __init__(self, auto_adjust=None, dimension_size=None):  # noqa: E501
        """NormalViewRestoredProperties - a model defined in Swagger"""  # noqa: E501

        self._auto_adjust = None
        self._dimension_size = None

        if auto_adjust is not None:
            self.auto_adjust = auto_adjust
        if dimension_size is not None:
            self.dimension_size = dimension_size

    @property
    def auto_adjust(self):
        """Gets the auto_adjust of this NormalViewRestoredProperties.  # noqa: E501

        True if the size of the side content region should compensate for the new size when resizing the window containing the view within the application.  # noqa: E501

        :return: The auto_adjust of this NormalViewRestoredProperties.  # noqa: E501
        :rtype: bool
        """
        return self._auto_adjust

    @auto_adjust.setter
    def auto_adjust(self, auto_adjust):
        """Sets the auto_adjust of this NormalViewRestoredProperties.

        True if the size of the side content region should compensate for the new size when resizing the window containing the view within the application.  # noqa: E501

        :param auto_adjust: The auto_adjust of this NormalViewRestoredProperties.  # noqa: E501
        :type: bool
        """
        self._auto_adjust = auto_adjust

    @property
    def dimension_size(self):
        """Gets the dimension_size of this NormalViewRestoredProperties.  # noqa: E501

        The size of the slide region.  # noqa: E501

        :return: The dimension_size of this NormalViewRestoredProperties.  # noqa: E501
        :rtype: float
        """
        return self._dimension_size

    @dimension_size.setter
    def dimension_size(self, dimension_size):
        """Sets the dimension_size of this NormalViewRestoredProperties.

        The size of the slide region.  # noqa: E501

        :param dimension_size: The dimension_size of this NormalViewRestoredProperties.  # noqa: E501
        :type: float
        """
        self._dimension_size = dimension_size

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
        if not isinstance(other, NormalViewRestoredProperties):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
