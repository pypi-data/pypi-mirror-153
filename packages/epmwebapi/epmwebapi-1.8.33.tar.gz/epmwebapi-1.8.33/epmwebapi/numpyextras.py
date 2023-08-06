"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import numpy as np
import datetime as dt
import dateutil.parser
import datetime
from datetime import timezone
from .basicvariable import DataTypeId

class NumpyExtras:

    def __init__(self):
      self._int = {}
      for i in range(60):
        self._int['{:02}'.format(i)] = i

    def numpyArrayFromDataValues(self, dataValues, sourceDataType = None):
        valuesCount = len(dataValues)
        i = 0

        dataType = float
        if (sourceDataType != None):
          dataType = self._getDataType(sourceDataType)
        else:
          while (i < valuesCount):
            if ('dataTypeId' in dataValues[i]):
              dataType = self._getDataType(dataValues[i]['dataTypeId'])
              break
            if (dataValues[i]['value'] != None):
              dataType = type(dataValues[i]['value'])
              break
            i = i + 1

        numpyArray = self._getNumpyArray(dataType, valuesCount)
        if valuesCount < 1:
            return numpyArray

        import time
        start_time = time.time()

        timestamps = map(self.fastValueToDateTime, [ x['timestamp'] for x in dataValues])
        numpyArray['Timestamp'].flat[:] = list(timestamps)

        numpyArray['Quality'].flat[:] = [ x['quality'] for x in dataValues]

        if dataType == float or dataType == int:
          numpyArray['Value'].flat[:] = list(map(lambda x: x['value'] if x['value'] != None else 0, dataValues))
        elif dataType == dt.datetime:
          timestamps = map(self.fastValueToDateTime, [ x['value'] for x in dataValues])
          numpyArray['Value'].flat[:] = list(timestamps)
        else:
          i = 0
          for numpyValue in numpyArray:
            dataValue = dataValues[i]
            if dataValue['value'] != None:
              numpyValue['Value'] = dataValue['value']
            i = i + 1

        return numpyArray

    def _getDataType(self, dataType):
      if (dataType == "i="+str(DataTypeId.Bit.value)):
        return bool
      elif (dataType == "i="+str(DataTypeId.DateTime.value)):
        return dt.datetime
      elif (dataType == "i="+str(DataTypeId.Double.value) or 
            dataType == "i="+str(DataTypeId.Float.value)):
        return float
      elif (dataType == "i="+str(DataTypeId.Int.value)):
        return int
      elif (dataType == "i="+str(DataTypeId.UInt.value)):
        return int
      elif (dataType == "i="+str(DataTypeId.String.value)):
        return str
      return float

    def _getNumpyArray(self, dataType, valuesCount):
        if dataType == int:
            return np.empty([valuesCount], dtype=np.dtype([('Value', '>i8'), ('Timestamp', 'object'), ('Quality', 'object')]))
        elif dataType == float:
            return np.empty([valuesCount], dtype=np.dtype([('Value', '>f4'), ('Timestamp', 'object'), ('Quality', 'object')]))
        elif dataType == bool:
            return np.empty([valuesCount], dtype=np.dtype([('Value', 'bool'), ('Timestamp', 'object'), ('Quality', 'object')]))
        elif dataType == str:
            return np.empty([valuesCount], dtype=np.dtype([('Value', 'object'), ('Timestamp', 'object'), ('Quality', 'object')]))
        elif dataType == dt.datetime:
            return np.empty([valuesCount], dtype=np.dtype([('Value', 'object'), ('Timestamp', 'object'), ('Quality', 'object')]))
        else: 
            return np.empty([valuesCount], dtype=np.dtype([('Value', '>f8'), ('Timestamp', 'object'), ('Quality', 'object')]))

    def fastValueToDateTime(self, item) -> datetime.datetime:
      val = item
      l = len(val)
      if (l == 23 or l == 24): #format == "%Y-%m-%dT%H:%M:%S.%fZ" and 
          us = int(val[20:(l - 1)])
          # If only milliseconds are given we need to convert to microseconds.
          if l == 23:
              us *= 10000
          if l == 24:
              us *= 1000
          return datetime.datetime(*map(int, [val[0:4], val[5:7], val[8:10], val[11:13], val[14:16], val[17:19]]), us, tzinfo=timezone.utc
          )
      elif (l == 20): #format == "%Y-%m-%dT%H:%M:%SZ" and 
          return datetime.datetime(*map(int, [val[0:4], val[5:7], val[8:10], val[11:13], val[14:16], val[17:19]]), 0, tzinfo=timezone.utc)
      else:
        return dateutil.parser.parse(val).astimezone(timezone.utc)

    def getDictValue(self, value):
      if value in self._int:
        return self._int[value]
      value = int(value)
      self._int[value] = value
      return value

