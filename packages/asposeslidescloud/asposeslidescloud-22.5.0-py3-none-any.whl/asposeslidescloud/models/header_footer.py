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

class HeaderFooter(ResourceBase):


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
        'is_date_time_visible': 'bool',
        'date_time_text': 'str',
        'is_footer_visible': 'bool',
        'footer_text': 'str',
        'is_slide_number_visible': 'bool'
    }

    attribute_map = {
        'self_uri': 'selfUri',
        'alternate_links': 'alternateLinks',
        'is_date_time_visible': 'isDateTimeVisible',
        'date_time_text': 'dateTimeText',
        'is_footer_visible': 'isFooterVisible',
        'footer_text': 'footerText',
        'is_slide_number_visible': 'isSlideNumberVisible'
    }

    type_determiners = {
    }

    def __init__(self, self_uri=None, alternate_links=None, is_date_time_visible=None, date_time_text=None, is_footer_visible=None, footer_text=None, is_slide_number_visible=None):  # noqa: E501
        """HeaderFooter - a model defined in Swagger"""  # noqa: E501
        super(HeaderFooter, self).__init__(self_uri, alternate_links)

        self._is_date_time_visible = None
        self._date_time_text = None
        self._is_footer_visible = None
        self._footer_text = None
        self._is_slide_number_visible = None

        if is_date_time_visible is not None:
            self.is_date_time_visible = is_date_time_visible
        if date_time_text is not None:
            self.date_time_text = date_time_text
        if is_footer_visible is not None:
            self.is_footer_visible = is_footer_visible
        if footer_text is not None:
            self.footer_text = footer_text
        if is_slide_number_visible is not None:
            self.is_slide_number_visible = is_slide_number_visible

    @property
    def is_date_time_visible(self):
        """Gets the is_date_time_visible of this HeaderFooter.  # noqa: E501

        True if date is displayed in the footer  # noqa: E501

        :return: The is_date_time_visible of this HeaderFooter.  # noqa: E501
        :rtype: bool
        """
        return self._is_date_time_visible

    @is_date_time_visible.setter
    def is_date_time_visible(self, is_date_time_visible):
        """Sets the is_date_time_visible of this HeaderFooter.

        True if date is displayed in the footer  # noqa: E501

        :param is_date_time_visible: The is_date_time_visible of this HeaderFooter.  # noqa: E501
        :type: bool
        """
        self._is_date_time_visible = is_date_time_visible

    @property
    def date_time_text(self):
        """Gets the date_time_text of this HeaderFooter.  # noqa: E501

        Text to be displayed as date in the footer  # noqa: E501

        :return: The date_time_text of this HeaderFooter.  # noqa: E501
        :rtype: str
        """
        return self._date_time_text

    @date_time_text.setter
    def date_time_text(self, date_time_text):
        """Sets the date_time_text of this HeaderFooter.

        Text to be displayed as date in the footer  # noqa: E501

        :param date_time_text: The date_time_text of this HeaderFooter.  # noqa: E501
        :type: str
        """
        self._date_time_text = date_time_text

    @property
    def is_footer_visible(self):
        """Gets the is_footer_visible of this HeaderFooter.  # noqa: E501

        True if footer is displayed  # noqa: E501

        :return: The is_footer_visible of this HeaderFooter.  # noqa: E501
        :rtype: bool
        """
        return self._is_footer_visible

    @is_footer_visible.setter
    def is_footer_visible(self, is_footer_visible):
        """Sets the is_footer_visible of this HeaderFooter.

        True if footer is displayed  # noqa: E501

        :param is_footer_visible: The is_footer_visible of this HeaderFooter.  # noqa: E501
        :type: bool
        """
        self._is_footer_visible = is_footer_visible

    @property
    def footer_text(self):
        """Gets the footer_text of this HeaderFooter.  # noqa: E501

        Text to be displayed in the footer  # noqa: E501

        :return: The footer_text of this HeaderFooter.  # noqa: E501
        :rtype: str
        """
        return self._footer_text

    @footer_text.setter
    def footer_text(self, footer_text):
        """Sets the footer_text of this HeaderFooter.

        Text to be displayed in the footer  # noqa: E501

        :param footer_text: The footer_text of this HeaderFooter.  # noqa: E501
        :type: str
        """
        self._footer_text = footer_text

    @property
    def is_slide_number_visible(self):
        """Gets the is_slide_number_visible of this HeaderFooter.  # noqa: E501

        True if slide number is displayed in the footer  # noqa: E501

        :return: The is_slide_number_visible of this HeaderFooter.  # noqa: E501
        :rtype: bool
        """
        return self._is_slide_number_visible

    @is_slide_number_visible.setter
    def is_slide_number_visible(self, is_slide_number_visible):
        """Sets the is_slide_number_visible of this HeaderFooter.

        True if slide number is displayed in the footer  # noqa: E501

        :param is_slide_number_visible: The is_slide_number_visible of this HeaderFooter.  # noqa: E501
        :type: bool
        """
        self._is_slide_number_visible = is_slide_number_visible

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
        if not isinstance(other, HeaderFooter):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
