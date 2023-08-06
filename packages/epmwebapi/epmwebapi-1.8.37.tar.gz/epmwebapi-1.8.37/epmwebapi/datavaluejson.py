"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import dateutil
import datetime
from datetime import timezone

class DataValueJSON(object):
    """description of class"""
    def __init__(self, value, statusCode, timestamp, dataTypeId=None):
        self._value = value
        self._statusCode = statusCode
        if type(timestamp) == str:
          try:
            self._timestamp = dateutil.parser.parse(timestamp).astimezone(timezone.utc)
          except OverflowError as error:
            self._timestamp = datetime.datetime(1,1,1,0,0,tzinfo=datetime.timezone.utc)
        else:
          self._timestamp = timestamp
        self._dataTypeId = dataTypeId

    @property
    def value(self):
      return self._value

    @property
    def statusCode(self):
      return self._statusCode

    @property
    def timestamp(self):
      return self._timestamp

    def toDict(self):
        value = self._value.isoformat() if type(self._value) == datetime.datetime else self._value
        if self._dataTypeId is None:
            return {'value': value, 'quality': self._statusCode,
                   'timestamp' : self._timestamp.isoformat()}
        else:
            return {'value': value, 'quality': self._statusCode,
                    'timestamp': self._timestamp.isoformat(), 'dataTypeId': self._dataTypeId}
