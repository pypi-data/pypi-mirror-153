"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from enum import Enum

class PerformUpdateType(Enum):

    Insert = 0

    Remove = 1

    Replace = 2

    Update = 3

