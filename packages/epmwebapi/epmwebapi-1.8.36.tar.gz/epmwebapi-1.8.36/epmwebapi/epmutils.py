"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from .datavaluejson import DataValueJSON
from .statuscodes import StatusCodes
import numpy
import copy

class EpmUtils:
    @staticmethod
    def translateQuality(dataValues):
        dataValuesCopy = copy.deepcopy(dataValues)
        if isinstance(dataValuesCopy, DataValueJSON):
            statusCode = dataValuesCopy.statusCode
            opcUa = EpmUtils._statusCodeToOpcUa(statusCode)
            dataValue = DataValueJSON(dataValuesCopy.value, opcUa, dataValuesCopy.timestamp)
            return dataValue
        elif isinstance(dataValuesCopy, dict):
            for numpyArray in dataValuesCopy.values():
                for num in numpyArray:
                    statusCode = num['Quality']
                    opcUa = EpmUtils._statusCodeToOpcUa(statusCode)
                    num['Quality'] = opcUa
            return dataValuesCopy
        elif isinstance(dataValuesCopy, numpy.ndarray):
            for num in dataValuesCopy:
                statusCode = num['Quality']
                opcUa = EpmUtils._statusCodeToOpcUa(statusCode)
                num['Quality'] = opcUa
            return dataValuesCopy
        else:
            raise Exception('Invalid dataValues parameter')

    @staticmethod
    def numpyToPandas(dataValues):
        import pandas
        dataValuesCopy = copy.deepcopy(dataValues)
        if isinstance(dataValuesCopy, dict):
            quality = numpy.ndarray
            timestamp = numpy.ndarray
            value = numpy.ndarray
            name = numpy.array
            first = True
            for numpyArray, varName in zip(dataValuesCopy.values(), dataValuesCopy.keys()):
                if first:
                    quality = numpyArray[:]['Quality'].byteswap().newbyteorder()
                    timestamp = numpyArray[:]['Timestamp']
                    value = numpyArray[:]['Value'].byteswap().newbyteorder()
                    name = numpy.array([varName] * len(numpyArray))
                    first = False
                else:
                    quality = numpy.append(quality, numpyArray[:]['Quality'].byteswap().newbyteorder())
                    timestamp = numpy.append(timestamp, numpyArray[:]['Timestamp'])
                    value = numpy.append(value, numpyArray[:]['Value'].byteswap().newbyteorder())
                    name = numpy.append(name, numpy.array([varName]*len(numpyArray)))
            d = {'Name': name, 'Value': value, 'Timestamp': timestamp, 'Quality': quality}
            dataValuesCopy = pandas.DataFrame(d)
            return dataValuesCopy
        elif isinstance(dataValuesCopy, numpy.ndarray):
            quality = dataValuesCopy[:]['Quality'].byteswap().newbyteorder()
            timestamp = dataValuesCopy[:]['Timestamp']
            value = dataValuesCopy[:]['Value'].byteswap().newbyteorder()

            d = {'Value': value, 'Timestamp': timestamp, 'Quality': quality}
            dataValuesCopy = pandas.DataFrame(d)
            return dataValuesCopy
        else:
            raise Exception('Invalid dataValues parameter')

    @staticmethod
    def _statusCodeToOpcUa(statusCode):
        for code in StatusCodes:
            if statusCode == code.value:
                return code.name
        return statusCode
