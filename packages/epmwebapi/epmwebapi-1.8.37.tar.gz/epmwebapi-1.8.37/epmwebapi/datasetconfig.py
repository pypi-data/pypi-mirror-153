"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import datetime
from enum import Enum
from dateutil.relativedelta import relativedelta
import re
import os
import ctypes

from .datasetpen import DatasetPen
from .queryperiod import QueryPeriod

class PeriodUnit(Enum):
    Second = 1

    Minute = 2

    Hour = 3

    Day = 4

    Month = 5


class DatasetConfig(object):
    """description of class"""

    REGEX_PATTERN = r'^[^a-z_]+|[^a-z0-9\.\:\%\&\@\!\-\#_]+|[^a-z0-9]+$|.{{{0},}}'
    NAME_MAX_SIZE = 50
    DESCRIPTION_MAX_SIZE = 500

    def __init__(self, connection, name, description = None):
        import os
        import clr
        clr.AddReference(os.path.dirname(os.path.abspath(__file__)) + '/dll_references/EpmData')

        from Elipse.Epm.Common import DatasetAndChartData, DatasetData

        self._connection = connection
        self._startTime = None
        self._endTime = None
        self._datasetPens = []
        self.setName(name)
        self.recentPeriodConfig(1, PeriodUnit.Hour)
        self._description = description
        self._datasetAndChartData = DatasetAndChartData(DatasetData(), '')

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def startTime(self):
      return self._startTime

    @property
    def endTime(self):
      return self._endTime

    @property
    def period(self):
        return self._period

    @property
    def isTimeInterval(self):
        return self._isTimeInterval

    @property
    def datasetPens(self):
      return self._datasetPens

    def setName(self, name):
        if type(name) is str:
            if len(name) > self.NAME_MAX_SIZE:
                raise Exception("Name cannot exceed " + str(self.NAME_MAX_SIZE) + " characters")
            elif re.search(self.REGEX_PATTERN, name):
                raise Exception("Invalid character on string argument")
            else:
                self._name = name
        else:
            raise Exception("Argument must be a string")

    def setDescription(self, description):
        if type(description) is str:
            if len(description) > self.DESCRIPTION_MAX_SIZE:
                raise Exception("Description cannot exceed " + str(self.DESCRIPTION_MAX_SIZE) + " characters")
            else:
                self._description = description
        else:
            raise Exception("Argument must be a string")

    def timeIntervalConfig(self, startTime, endTime):
        if isinstance(startTime, datetime.datetime) and isinstance(endTime, datetime.datetime):
            import pytz
            startTimeUtc = startTime.astimezone(pytz.UTC)
            endTimeUtc = endTime.astimezone(pytz.UTC)
            if startTimeUtc < endTimeUtc:
                self._startTime = startTimeUtc
                self._endTime = endTimeUtc
                self._isTimeInterval = True
            else:
                raise Exception("startTime must be before endTime")
        else:
            raise Exception("Arguments must be of datetime type")

    def recentPeriodConfig(self, count, periodUnit):
        if not isinstance(count, int):
            raise Exception("count argument must be an integer")
        if not isinstance(periodUnit, PeriodUnit):
            raise Exception("periodUnit argument must be of type PeriodUnit")
        self._periodXmlToTimePeriod(count, periodUnit.value)
        self._isTimeInterval = False

    def addPen(self, title, dataSourceName = None):
        for pen in self._datasetPens:
            if pen.title == title:
                raise Exception("Pen title already exists")
        datasetPen = DatasetPen(self, title, dataSourceName)
        self._datasetPens.append(datasetPen)
        return self.getPen(title)

    def getPen(self, title):
        for pen in self._datasetPens:
            if pen.title == title:
                return pen
        raise Exception("Pen not found")

    def removePen(self, title):
        for pen in self._datasetPens:
            if pen.title == title:
                self._datasetPens.remove(pen)
                return
        raise Exception("Pen not found")

    def execute(self):
        results = {}

        if self.isTimeInterval:
            queryPeriod = QueryPeriod(self.startTime, self.endTime)
        else:
            import pytz
            endTime = datetime.datetime.utcnow()
            endTime = pytz.UTC.localize(endTime)
            startTime = endTime - self.period
            queryPeriod = QueryPeriod(startTime, endTime)

        for pen in self.datasetPens:
            pen.setDataSource(pen.dataSource.name)
            if pen.isRaw:
                result = self._connection._historyReadRaw(queryPeriod, pen.dataSource._itemPath)
            else:
                result = self._connection._historyReadAggregate(pen.aggregateType, queryPeriod, pen.dataSource._itemPath)
            results[pen.title] = result

        return results

    def saveToFile(self, path, overwrite = False):
        if path.endswith('/'):
            filePath = path + self.name + ".epmdataset"
        else:
            filePath = path + '/' + self.name + ".epmdataset"
        epmExtensionXml = self._getEpmExtensionXmlLocal()
        self._connection._saveDatasetFile(epmExtensionXml, filePath, overwrite=overwrite)
        self.__class__ = DatasetConfigLocal
        self._filePath = filePath

    def saveToLocal(self, overwrite = False):
        CSIDL_PERSONAL = 5  # My Documents
        SHGFP_TYPE_CURRENT = 0  # Get current, not default value
        documentsFolder = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, documentsFolder)
        documentsFolder = documentsFolder.value.replace('\\', '/')
        filePath = documentsFolder + '/Elipse Software/EPM Studio/Datasets/' + self.name + ".epmdataset"
        epmExtensionXml = self._getEpmExtensionXmlLocal()
        self._connection._saveDatasetFile(epmExtensionXml, filePath, overwrite=overwrite)
        self.__class__ = DatasetConfigLocal
        self._filePath = filePath

    def saveToServer(self, overwrite = False):
        epmExtensionXml = self._getEpmExtensionXmlServer()
        self._connection._saveDatasetServer(self.name, self.description, epmExtensionXml, overwrite=overwrite)
        self.__class__ = DatasetConfigServer

    def _getEpmExtensionXmlLocal(self):
        import os
        import clr
        clr.AddReference(os.path.dirname(os.path.abspath(__file__)) + '/dll_references/EpmData')
        from Elipse.Epm.Common import TimeInterval, RecentPeriod, DatasetField, RawByPeriod, TrendMode, CalculateMode, \
            EpmExtensionObject, DatasetAndChartData, FileContentData, DatasetData
        from Elipse.Epm.AddressSpaceModel import NodeIdentifier
        from System import DateTime, TimeSpan
        from System.Collections.Generic import List

        if self.isTimeInterval:
            period = TimeInterval()
            period.StartTime = DateTime.Parse(str(self.startTime))
            period.EndTime = DateTime.Parse(str(self.endTime))
        else:
            period = RecentPeriod()
            period.Count = self._count
            period.PeriodType = self._periodUnit

        fields = []
        for datasetPen in self._datasetPens:
            pen = DatasetField()
            pen.Alias = datasetPen.title
            if datasetPen.isRaw:
                pen.Mode = RawByPeriod()
            else:
                sampleInterval = TimeSpan.Parse(str(datasetPen.aggregateType.interval))
                aggregateType = datasetPen._getAggregateId()
                if aggregateType == 1:
                    pen.Mode = TrendMode(sampleInterval)
                else:
                    pen.Mode = CalculateMode(aggregateType, sampleInterval)
            nodeId = datasetPen.dataSource._identity
            identifier = int(nodeId.split(';')[1].split('=')[1])
            namespaceIndex = int(nodeId.split(';')[0].split('=')[1])
            pen.Identity = NodeIdentifier()
            pen.Identity.IdentifierType = 1
            pen.Identity.Numeric32Identifier = identifier
            pen.Identity.NamespaceIndex = namespaceIndex
            fields.append(pen)

        self._datasetAndChartData.Dataset.Period = period
        fieldsList = List[DatasetField]()
        for field in fields:
            fieldsList.Add(field)
        self._datasetAndChartData.Dataset.Fields = fieldsList

        epmExtensionObject = EpmExtensionObject(self._datasetAndChartData.ToXml())
        epmExtensionObject.Tag = DatasetAndChartData.Tag
        epmExtensionXml = epmExtensionObject.ToXml()

        fileContent = FileContentData(self.description, epmExtensionXml)
        fileContentXml = fileContent.ToXml()

        epmExtensionObject = EpmExtensionObject()
        epmExtensionObject.Tag = FileContentData.Tag
        epmExtensionObject.Content = fileContentXml
        epmExtensionXml = epmExtensionObject.ToXml()

        return epmExtensionXml

    def _getEpmExtensionXmlServer(self):
        import os
        import clr
        clr.AddReference(os.path.dirname(os.path.abspath(__file__)) + '/dll_references/EpmData')
        from Elipse.Epm.Common import TimeInterval, RecentPeriod, DatasetField, RawByPeriod, TrendMode, CalculateMode, \
            EpmExtensionObject, DatasetAndChartData, FileContentData, DatasetData
        from Elipse.Epm.AddressSpaceModel import NodeIdentifier
        from System import DateTime, TimeSpan
        from System.Collections.Generic import List

        if self.isTimeInterval:
            period = TimeInterval()
            period.StartTime = DateTime.Parse(str(self.startTime))
            period.EndTime = DateTime.Parse(str(self.endTime))
        else:
            period = RecentPeriod()
            period.Count = self._count
            period.PeriodType = self._periodUnit

        fields = []
        for datasetPen in self._datasetPens:
            pen = DatasetField()
            pen.Alias = datasetPen.title
            if datasetPen.isRaw:
                pen.Mode = RawByPeriod()
            else:
                sampleInterval = TimeSpan.Parse(str(datasetPen.aggregateType.interval))
                aggregateType = datasetPen._getAggregateId()
                if aggregateType == 1:
                    pen.Mode = TrendMode(sampleInterval)
                else:
                    pen.Mode = CalculateMode(aggregateType, sampleInterval)
            nodeId = datasetPen.dataSource._itemPath._relativePath
            identifier = int(nodeId.split(';')[1].split('=')[1])
            namespaceIndex = int(nodeId.split(';')[0].split('=')[1])
            pen.Identity = NodeIdentifier()
            pen.Identity.IdentifierType = 1
            pen.Identity.Numeric32Identifier = identifier
            pen.Identity.NamespaceIndex = namespaceIndex
            fields.append(pen)

        self._datasetAndChartData.Dataset.Period = period
        fieldsList = List[DatasetField]()
        for field in fields:
            fieldsList.Add(field)
        self._datasetAndChartData.Dataset.Fields = fieldsList

        epmExtensionObject = EpmExtensionObject(self._datasetAndChartData.ToXml())
        epmExtensionObject.Tag = DatasetAndChartData.Tag
        epmExtensionXml = epmExtensionObject.ToXml()

        return epmExtensionXml

    def _periodXmlToTimePeriod(self, count, period):
        if period == 1:
            self._period = datetime.timedelta(seconds=count)
        elif period == 2:
            self._period = datetime.timedelta(minutes=count)
        elif period == 3:
            self._period = datetime.timedelta(hours=count)
        elif period == 4:
            self._period = datetime.timedelta(days=count)
        elif period == 5:
            self._period = relativedelta(months=count)
        else:
            raise Exception("Error with the period time unit")
        self._count = count
        self._periodUnit = period

    def _convertToPyDateTime(self, dateTime):
        import dateutil.parser
        import pytz
        strDateTime = dateTime.ToString()
        try:
            pyDateTime = datetime.datetime.strptime(strDateTime, '%m/%d/%Y %H:%M:%S %p')
        except:
            try:
                pyDateTime = datetime.datetime.strptime(strDateTime, '%d/%m/%Y %H:%M:%S')
            except:
                pyDateTime = dateutil.parser.parse(strDateTime)
        finally:
            pyDateTime = pytz.UTC.localize(pyDateTime)
            return pyDateTime

class DatasetConfigLocal(DatasetConfig):
    """description of class"""
    def __init__(self, connection, name, content = None, description = None, filePath = None):
        import os
        import clr
        clr.AddReference(os.path.dirname(os.path.abspath(__file__)) + '/dll_references/EpmData')
        from Elipse.Epm.Common import EpmExtensionObject, SerializationExtensions, TimeInterval, DatasetAndChartData, \
                                      DatasetData
        self._connection = connection
        self._name = None
        self._count = None
        self._periodUnit = None
        self._startTime = None
        self._endTime = None
        self._period = None
        self._datasetPens = []
        self._filePath = filePath
        self._nameChanged = False
        if content is None:
            self.setName(name)
            self.recentPeriodConfig(1, PeriodUnit.Hour)
            self._description = description
            self._datasetAndChartData = DatasetAndChartData(DatasetData(), '')
        else:
            self._name = name
            contentObject = EpmExtensionObject.FromXml(content)
            resource = SerializationExtensions.ReadFileResourceContent(contentObject)
            self._description = resource.Description
            resourceObject = EpmExtensionObject.FromXml(resource.Content)
            dataset = SerializationExtensions.ReadDatasetAndChartData(resourceObject)
            self._datasetAndChartData = dataset

            periodType = dataset.Dataset.Period
            if isinstance(periodType, TimeInterval):
                self._isTimeInterval = True
                start = dataset.Dataset.Period.StartTime
                startUtc = start.ToUniversalTime()
                startTime = self._convertToPyDateTime(startUtc)
                self._startTime = startTime
                end = dataset.Dataset.Period.EndTime
                endUtc = end.ToUniversalTime()
                endTime = self._convertToPyDateTime(endUtc)
                self._endTime = endTime
            else:
                self._isTimeInterval = False
                count = dataset.Dataset.Period.Count
                period = dataset.Dataset.Period.PeriodType
                self._periodXmlToTimePeriod(count, period)


            for penConfig in dataset.Dataset.Fields:
                title = penConfig.Alias
                self._datasetPens.append(DatasetPen(self, title, penConfig=penConfig))

    @property
    def filePath(self):
        return self._filePath

    def setName(self, name):
        if type(name) is str:
            if len(name) > self.NAME_MAX_SIZE:
                raise Exception("Name cannot exceed " + str(self.NAME_MAX_SIZE) + " characters")
            elif re.search(self.REGEX_PATTERN, name):
                raise Exception("Invalid character on string argument")
            else:
                if name != self.name:
                    self._name = name
                    self._nameChanged = True
        else:
            raise Exception("Argument must be a string")

    def save(self):
        epmExtensionXml = self._getEpmExtensionXmlLocal()
        if self._filePath is not None:
            if self._nameChanged:
                pathSplit = self._filePath.split("/")
                pathSplit.pop(-1)
                path = '/'.join(pathSplit)
                newFilePath = path + '/' + self.name + ".epmdataset"
                if os.path.exists(newFilePath):
                    raise Exception("Dataset name changed but there is another dataset with this name on the same folder")
                self._connection._saveDatasetFile(epmExtensionXml, self._filePath, overwrite=True)
                os.rename(self._filePath, newFilePath)
                self._filePath = newFilePath
                self._nameChanged = False
            else:
                self._connection._saveDatasetFile(epmExtensionXml, self._filePath, overwrite=True)
        else:
            raise Exception("There is no dataset file to save, use the method saveToFile() or saveToLocal() instead")

    def delete(self):
        self._connection._deleteDatasetFile(self._filePath)
        self.__class__ = DatasetConfig

    def duplicate(self, newName, samePath = True):
        duplicate = DatasetConfigLocal(self._connection, self.name, self._getEpmExtensionXmlLocal())
        duplicate.setName(newName)
        if samePath:
            if self._filePath is None:
                raise Exception("Dataset has no file on folder")
            pathSplit = self._filePath.split("/")
            pathSplit.pop(-1)
            path = '/'.join(pathSplit)
            newFilePath = path + '/' + newName + ".epmdataset"
            if os.path.exists(newFilePath):
                raise Exception("Dataset name already exists on that folder")
            duplicate._filePath = newFilePath
        else:
            duplicate._filePath = None

        return duplicate


class DatasetConfigServer(DatasetConfig):
    """description of class"""
    def __init__(self, connection, name, description, content = None):
        import os
        import clr
        clr.AddReference(os.path.dirname(os.path.abspath(__file__)) + '/dll_references/EpmData')
        from Elipse.Epm.Common import EpmExtensionObject, SerializationExtensions, TimeInterval, DatasetAndChartData, \
                                      DatasetData
        self._connection = connection
        self._name = None
        self._description = description
        self._count = None
        self._periodUnit = None
        self._startTime = None
        self._endTime = None
        self._period = None
        self._datasetPens = []
        self._nameChanged = False
        self._oldName = None
        if content is None:
            self.setName(name)
            self.recentPeriodConfig(1, PeriodUnit.Hour)
            self._datasetAndChartData = DatasetAndChartData(DatasetData(), '')
        else:
            self._name = name
            resourceObject = EpmExtensionObject.FromXml(content)
            dataset = SerializationExtensions.ReadDatasetAndChartData(resourceObject)
            self._datasetAndChartData = dataset

            periodType = dataset.Dataset.Period
            if isinstance(periodType, TimeInterval):
                self._isTimeInterval = True
                start = dataset.Dataset.Period.StartTime
                startUtc = start.ToUniversalTime()
                startTime = self._convertToPyDateTime(startUtc)
                self._startTime = startTime
                end = dataset.Dataset.Period.EndTime
                endUtc = end.ToUniversalTime()
                endTime = self._convertToPyDateTime(endUtc)
                self._endTime = endTime
            else:
                self._isTimeInterval = False
                count = dataset.Dataset.Period.Count
                period = dataset.Dataset.Period.PeriodType
                self._periodXmlToTimePeriod(count, period)


            for penConfig in dataset.Dataset.Fields:
                title = penConfig.Alias
                self._datasetPens.append(DatasetPen(self, title, penConfig=penConfig))

    def setName(self, name):
        if type(name) is str:
            if len(name) > self.NAME_MAX_SIZE:
                raise Exception("Name cannot exceed " + str(self.NAME_MAX_SIZE) + " characters")
            if re.search(self.REGEX_PATTERN, name):
                raise Exception("Invalid character on string argument")
            else:
                if name != self.name:
                    self._oldName = self._name
                    self._name = name
                    self._nameChanged = True
        else:
            raise Exception("Argument must be a string")

    def save(self):
        epmExtensionXml = self._getEpmExtensionXmlServer()
        if self._nameChanged:
            for datasetName in self._connection.listDatasetServer():
                if str.lower(self.name) == str.lower(datasetName):
                    raise Exception("Dataset name changed but there is another dataset with this name on server")
            if self._oldName is None:
                self._connection._saveDatasetServer(self.name, self.description, epmExtensionXml)
            else:
                self._connection._saveDatasetServer(self.name, self.description, epmExtensionXml, oldName=self._oldName)
            self._nameChanged = False
        else:
            self._connection._saveDatasetServer(self.name, self.description, epmExtensionXml, overwrite=True)

    def delete(self):
        self._connection._deleteDatasetServer(self.name)
        self.__class__ = DatasetConfig

    def duplicate(self, newName):
        duplicate = DatasetConfigServer(self._connection, self.name, self.description, content=self._getEpmExtensionXmlServer())
        if newName == self.name:
            raise Exception("Duplicated dataset must have a different name")
        for datasetName in self._connection.listDatasetServer():
            if str.lower(newName) == str.lower(datasetName):
                raise Exception("There is another dataset with this name on server")
        duplicate.setName(newName)
        duplicate._oldName = None

        return duplicate

