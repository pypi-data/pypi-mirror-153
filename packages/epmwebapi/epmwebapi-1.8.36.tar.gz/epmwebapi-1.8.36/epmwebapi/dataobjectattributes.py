"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from enum import IntFlag

class DataObjectAttributes(IntFlag):

    Unspecified = 0

    Name = 1

    Description = 2

    EU = 4

    LowLimit = 8

    HighLimit = 16

    Clamping = 32

    Domain = 64

    Active = 128

    TagType = 256

    All = 65535

