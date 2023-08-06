"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from enum import Enum

class QueryResultMask(Enum):

    Unknown = 0

    Identity = 1

    Name = 2

    Description = 4

    Type = 8

    All = 31

