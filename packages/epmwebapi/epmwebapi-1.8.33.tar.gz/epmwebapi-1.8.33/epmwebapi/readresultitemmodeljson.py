"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

class ReadResultItemModelJSON(object):

  def __init__(self, identity, value):
    self._identity = identity
    self._value = value

  @property
  def identity(self):
      return self._identity

  @property
  def value(self):
      return self._value

