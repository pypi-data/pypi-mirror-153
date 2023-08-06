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


class ChartCategory(object):


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'parent_categories': 'list[str]',
        'level': 'int',
        'value': 'str',
        'fill_format': 'FillFormat',
        'effect_format': 'EffectFormat',
        'line_format': 'LineFormat',
        'data_points': 'list[OneValueChartDataPoint]'
    }

    attribute_map = {
        'parent_categories': 'parentCategories',
        'level': 'level',
        'value': 'value',
        'fill_format': 'fillFormat',
        'effect_format': 'effectFormat',
        'line_format': 'lineFormat',
        'data_points': 'dataPoints'
    }

    type_determiners = {
    }

    def __init__(self, parent_categories=None, level=None, value=None, fill_format=None, effect_format=None, line_format=None, data_points=None):  # noqa: E501
        """ChartCategory - a model defined in Swagger"""  # noqa: E501

        self._parent_categories = None
        self._level = None
        self._value = None
        self._fill_format = None
        self._effect_format = None
        self._line_format = None
        self._data_points = None

        if parent_categories is not None:
            self.parent_categories = parent_categories
        if level is not None:
            self.level = level
        if value is not None:
            self.value = value
        if fill_format is not None:
            self.fill_format = fill_format
        if effect_format is not None:
            self.effect_format = effect_format
        if line_format is not None:
            self.line_format = line_format
        if data_points is not None:
            self.data_points = data_points

    @property
    def parent_categories(self):
        """Gets the parent_categories of this ChartCategory.  # noqa: E501

        Gets or sets the parent categories. Used with Sunburst &amp; treemap categories; ignored for other chart types.  # noqa: E501

        :return: The parent_categories of this ChartCategory.  # noqa: E501
        :rtype: list[str]
        """
        return self._parent_categories

    @parent_categories.setter
    def parent_categories(self, parent_categories):
        """Sets the parent_categories of this ChartCategory.

        Gets or sets the parent categories. Used with Sunburst &amp; treemap categories; ignored for other chart types.  # noqa: E501

        :param parent_categories: The parent_categories of this ChartCategory.  # noqa: E501
        :type: list[str]
        """
        self._parent_categories = parent_categories

    @property
    def level(self):
        """Gets the level of this ChartCategory.  # noqa: E501

        Gets or sets the grouping level for the category. Used with Sunburst &amp; treemap categories; ignored for other chart types.  # noqa: E501

        :return: The level of this ChartCategory.  # noqa: E501
        :rtype: int
        """
        return self._level

    @level.setter
    def level(self, level):
        """Sets the level of this ChartCategory.

        Gets or sets the grouping level for the category. Used with Sunburst &amp; treemap categories; ignored for other chart types.  # noqa: E501

        :param level: The level of this ChartCategory.  # noqa: E501
        :type: int
        """
        self._level = level

    @property
    def value(self):
        """Gets the value of this ChartCategory.  # noqa: E501

        Category value  # noqa: E501

        :return: The value of this ChartCategory.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this ChartCategory.

        Category value  # noqa: E501

        :param value: The value of this ChartCategory.  # noqa: E501
        :type: str
        """
        self._value = value

    @property
    def fill_format(self):
        """Gets the fill_format of this ChartCategory.  # noqa: E501

        Get or sets the fill format.  # noqa: E501

        :return: The fill_format of this ChartCategory.  # noqa: E501
        :rtype: FillFormat
        """
        return self._fill_format

    @fill_format.setter
    def fill_format(self, fill_format):
        """Sets the fill_format of this ChartCategory.

        Get or sets the fill format.  # noqa: E501

        :param fill_format: The fill_format of this ChartCategory.  # noqa: E501
        :type: FillFormat
        """
        self._fill_format = fill_format

    @property
    def effect_format(self):
        """Gets the effect_format of this ChartCategory.  # noqa: E501

        Get or sets the effect format.  # noqa: E501

        :return: The effect_format of this ChartCategory.  # noqa: E501
        :rtype: EffectFormat
        """
        return self._effect_format

    @effect_format.setter
    def effect_format(self, effect_format):
        """Sets the effect_format of this ChartCategory.

        Get or sets the effect format.  # noqa: E501

        :param effect_format: The effect_format of this ChartCategory.  # noqa: E501
        :type: EffectFormat
        """
        self._effect_format = effect_format

    @property
    def line_format(self):
        """Gets the line_format of this ChartCategory.  # noqa: E501

        Get or sets the line format.  # noqa: E501

        :return: The line_format of this ChartCategory.  # noqa: E501
        :rtype: LineFormat
        """
        return self._line_format

    @line_format.setter
    def line_format(self, line_format):
        """Sets the line_format of this ChartCategory.

        Get or sets the line format.  # noqa: E501

        :param line_format: The line_format of this ChartCategory.  # noqa: E501
        :type: LineFormat
        """
        self._line_format = line_format

    @property
    def data_points(self):
        """Gets the data_points of this ChartCategory.  # noqa: E501

        Gets or sets the data points for chart data  # noqa: E501

        :return: The data_points of this ChartCategory.  # noqa: E501
        :rtype: list[OneValueChartDataPoint]
        """
        return self._data_points

    @data_points.setter
    def data_points(self, data_points):
        """Sets the data_points of this ChartCategory.

        Gets or sets the data points for chart data  # noqa: E501

        :param data_points: The data_points of this ChartCategory.  # noqa: E501
        :type: list[OneValueChartDataPoint]
        """
        self._data_points = data_points

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
        if not isinstance(other, ChartCategory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
