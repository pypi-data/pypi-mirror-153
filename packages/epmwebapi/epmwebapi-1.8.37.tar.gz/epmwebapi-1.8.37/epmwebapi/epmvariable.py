"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from .itempathjson import ItemPathJSON
import datetime as dt
from .datavaluejson import DataValueJSON
from .historyupdatetype import HistoryUpdateType

class EpmVariable(object):
    """description of class"""

    def __init__(self, epmConnection, name, path, itemPath):
      self._epmConnection = epmConnection
      self._name = name
      self._path = path
      self._itemPath = itemPath

    ### Properties
    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    ### Methods

    def historyReadRaw(self, queryPeriod, bounds = False):
        return self._epmConnection._historyReadRaw(queryPeriod, self._itemPath, bounds = bounds)

    def read(self):
        readResult = self._epmConnection._read([self._itemPath], [13]).items()[0]
        if readResult[1].code != 0:
          raise Exception("Read from '" + self._path + "' failed with error: " + str(readResult[1].code))
        return readResult[0].value

    def write(self, value, timestamp=dt.datetime.now(dt.timezone.utc), quality=0):
        return self._epmConnection._write([self._itemPath], [13], [DataValueJSON(value, quality, timestamp)])

    def historyReadAggregate(self, aggregateDetails, queryPeriod):
        return self._epmConnection._historyReadAggregate(aggregateDetails, queryPeriod, self._itemPath)

    def historyUpdate(self, values):
        return self._epmConnection._historyUpdate(HistoryUpdateType.Update.value, [ self._itemPath ], [ values ])

    def historyDelete(self, queryPeriod):
        values = self._epmConnection._historyReadRaw(queryPeriod, self._itemPath, False)
        return self._epmConnection._historyUpdate(HistoryUpdateType.Remove.value, [ self._itemPath ], [ values ])


