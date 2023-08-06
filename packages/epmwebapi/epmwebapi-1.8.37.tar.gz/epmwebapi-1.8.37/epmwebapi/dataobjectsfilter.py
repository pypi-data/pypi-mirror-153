"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from .domainfilter import DomainFilter

from enum import IntFlag


class DataObjectsFilterType(IntFlag):

  BasicVariable = 1

  ExpressionVariable = 2


class DataObjectsFilter(object):
  """description of class"""

  def __init__(self, type = None, name = None, eu = None, description = None, domain = None):
    self._type = DataObjectsFilterType.BasicVariable | DataObjectsFilterType.ExpressionVariable if type == None else type
    self._name = '*' if name == None else name
    self._eu = '*' if eu == None else eu
    self._description = description
    self._domain = DomainFilter.All if domain == None else domain

  @property
  def type(self):
    return self._type

  @property
  def name(self):
    return self._name
  
  @property
  def eu(self):
    return self._eu

  @property
  def description(self):
    return self._description

  @property
  def domain(self):
    return self._domain
