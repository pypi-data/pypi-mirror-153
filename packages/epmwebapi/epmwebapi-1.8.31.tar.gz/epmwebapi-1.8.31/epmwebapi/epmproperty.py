"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from .itempathjson import ItemPathJSON
import datetime as dt
from .datavaluejson import DataValueJSON
from .epmvariable import EpmVariable

class EpmProperty(EpmVariable):
    """description of class"""

    def __init__(self, epmConnection, name, path, itemPath):
        super().__init__(epmConnection, name, path, itemPath)






