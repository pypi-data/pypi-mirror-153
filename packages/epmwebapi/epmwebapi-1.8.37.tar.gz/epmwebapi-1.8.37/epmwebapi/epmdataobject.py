"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""
import pytz

from .itempathjson import ItemPathJSON
import datetime as dt
from .queryperiod import QueryPeriod
from .datavaluejson import DataValueJSON
from .epmvariable import EpmVariable
from .epmproperty import EpmProperty
from .dataobjectattributes import DataObjectAttributes
from .epmnodeids import EpmNodeIds
from .basicvariablepropertymask import BasicVariablePropertyMask

from enum import Enum
import collections


class EpmDataObjectPropertyNames(Enum):
    Name = "4:Name"

    Description = "4:Description"

    EU = "0:EngineeringUnits"

    LowLimit = "4:RangeLow"

    HighLimit = "4:RangeHigh"

    Clamping = "4:RangeClamping"

    Domain = "4:Discrete"

    Annotations = "4:Annotations"


class EpmDataObjectAttributeIds(Enum):
    Name = 1

    Description = 2

    TagType = 3

    LowLimit = 15

    HighLimit = 16

    Clamping = 17

    Domain = 21

    EU = 22

    Active = 23

    Annotations = 900


class RetrievalMode(Enum):
    Previous = "Previous"

    Exact = "Exact"

    Next = "Next"


class ClampingMode(Enum):
    NoneClamping = 0

    Discard = 1

    ClampToRange = 2


def getDiscreteValue(domain):
  if domain == 'Discrete':
    return True
  elif domain == 'Continuous':
    return False
  else:
    return None

def getDomainValue(discrete):
  if discrete == None:
    return None
  elif discrete:
    return 'Discrete'
  else:
    return 'Continuous'

class EpmDataObject(EpmVariable):
    """description of class"""

    def __init__(self, epmConnection, name, itemPath):
        super().__init__(epmConnection, name, '/DataObjects/' + name, itemPath)
        self._changeMask = BasicVariablePropertyMask.Unspecified.value
        self._itemPath = itemPath
        self._description = None
        self._eu = None
        self._highLimit = None
        self._lowLimit = None
        self._clamping = None
        self._domain = None
        self._active = None

    ### Properties
    @property
    def description(self):
      return self._description

    @description.setter
    def description(self, value):
      if self._description == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.Description.value
      self._description = value

    @property
    def eu(self):
      return self._eu

    @eu.setter
    def eu(self, value):
      if self._eu == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.Eu.value
      self._eu = value

    @property
    def lowLimit(self):
      return self._lowLimit

    @lowLimit.setter
    def lowLimit(self, value):
      if self._lowLimit == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.LowLimit.value
      self._lowLimit = value

    @property
    def highLimit(self):
      return self._highLimit

    @highLimit.setter
    def highLimit(self, value):
      if self._highLimit == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.HighLimit.value
      self._highLimit = value

    @property
    def clamping(self):
      return ClampingMode(self._clamping) if self._clamping is not None else None

    @clamping.setter
    def clamping(self, value):
        if isinstance(value, int) or value is None:
            if self._clamping == value:
                return
            self._clamping = value
        else:
            if self._clamping == value.value:
                return
            self._clamping = value.value
        self._changeMask = self._changeMask | BasicVariablePropertyMask.Clamping.value

    @property
    def domain(self):
      return self._domain

    @domain.setter
    def domain(self, value):
      if self._domain == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.Domain.value
      self._domain = value

    @property
    def active(self):
        return self._active


    ## Public Methods
    def recordedValue(self, timestamp, retrieval = RetrievalMode.Previous):
        timestamp = timestamp.astimezone(pytz.UTC)
        start = timestamp - dt.timedelta(milliseconds=1)
        end = timestamp + dt.timedelta(milliseconds=1)
        queryPeriod = QueryPeriod(start, end)
        result = self.historyReadRaw(queryPeriod, True)

        previousVal = None
        exactVal = None
        nextVal = None

        if result.size == 1:
            if result[0][1] > timestamp:
                nextVal = result[0]
            elif result[0][1] == timestamp:
                exactVal = result[0]
            else:
                previousVal = result[0]
        elif result.size == 2:
            if result[1][1] > timestamp:
                nextVal = result[1]
            elif result[1][1] == timestamp:
                exactVal = result[1]
            if result[0][1] < timestamp:
                previousVal = result[0]
            elif result[0][1] == timestamp:
                exactVal = result[0]
        elif result.size == 3:
            previousVal = result[0]
            exactVal = result[1]
            nextVal = result[2]
        elif result.size == 4:
            previousVal = result[1]
            exactVal = result[2]
            nextVal = result[3]
        else:
            return None

        if retrieval == RetrievalMode.Previous:
            if previousVal and previousVal[2] == 2156527616:
                return self.recordedValue(previousVal[1], retrieval)
            else:
                return previousVal
        elif retrieval == RetrievalMode.Exact:
            if exactVal and exactVal[2] == 2156527616:
                return None
            else:
                return exactVal
        elif retrieval == RetrievalMode.Next:
            if nextVal and nextVal[2] == 2156527616:
                return self.recordedValue(nextVal[1], retrieval)
            else:
                return nextVal

    def readAnnotations(self, start, end):
      queryPeriod = QueryPeriod(start, end)
      annotationPath = ItemPathJSON('OPCUA.NodeId', None, self._encodePropertyIdentity(EpmDataObjectAttributeIds.Annotations.value))
      return self._epmConnection._historyReadAnnotation(queryPeriod, annotationPath)

    def deleteAnnotations(self, start, end, allUsers = False):
      userName = self._epmConnection._authorizationService._userName
      result = self.readAnnotations(start, end)
      deletedItems = []
      for index in range(len(result)):
        if allUsers or result[index][1] == userName:
          deletedItems.append(result[index])

      if len(deletedItems) == 0:
        return

      annotationPath = ItemPathJSON('OPCUA.NodeId', None, self._encodePropertyIdentity(EpmDataObjectAttributeIds.Annotations.value))
      from .performupdatetype import PerformUpdateType
      self._epmConnection._historyUpdateAnnotation(annotationPath, PerformUpdateType.Remove.value, deletedItems)

    def writeAnnotation(self, timestamp, message, override = True):
      timestamp = timestamp.astimezone(pytz.UTC)
      annotationPath = ItemPathJSON('OPCUA.NodeId', None, self._encodePropertyIdentity(EpmDataObjectAttributeIds.Annotations.value))
      userName = self._epmConnection._authorizationService._context._userName
      annotations = [ (timestamp, userName, message) ]
      from .performupdatetype import PerformUpdateType
      if override:
        results = self.readAnnotations(timestamp, timestamp + dt.timedelta(seconds=1))
        for index in range(len(results)):
          if results[index][1] == userName and self._compareDatetime(results[index][0].astimezone(pytz.UTC), timestamp):
            return self._epmConnection._historyUpdateAnnotation(annotationPath, PerformUpdateType.Update.value, annotations)
      return self._epmConnection._historyUpdateAnnotation(annotationPath, PerformUpdateType.Insert.value, annotations)

    def readAttributes(self):
      self._epmConnection._fillDataObjectsAttributes([ self ], DataObjectAttributes.All)

    def enumProperties(self):
      result = self._epmConnection._browse([ self._itemPath ], EpmNodeIds.HasProperty.value).references()
      childProperties = collections.OrderedDict()
      for item in result[0]:
        childProperties[item._displayName] = EpmProperty(self._epmConnection, item._displayName, self._path + '/' + item._displayName, item._identity)
      return childProperties

    def _compareDatetime(self, datetime1, datetime2):
      return (datetime1.year == datetime2.year and
              datetime1.month == datetime2.month and
              datetime1.day == datetime2.day and
              datetime1.hour == datetime2.hour and
              datetime1.minute == datetime2.minute and
              datetime1.second == datetime2.second and
              datetime1.microsecond == datetime2.microsecond)

    def _setAttribute(self, attributeId, value):
      if attributeId == DataObjectAttributes.Description:
        self._description = value if value is not None else ""
      elif attributeId == DataObjectAttributes.EU:
        self._eu = value['displayName'] if value is not None else value
      elif attributeId == DataObjectAttributes.HighLimit:
        self._highLimit = value
      elif attributeId == DataObjectAttributes.LowLimit:
        self._lowLimit = value
      elif attributeId == DataObjectAttributes.Clamping:
        self._clamping = value
      elif attributeId == DataObjectAttributes.Domain:
        self._domain = 'Discrete' if value else 'Continuous'
      elif attributeId == DataObjectAttributes.Active:
        self._active = value


    #Private Methods
    def _encodePropertyIdentity(self, propertyIdentity):

      nodeIdSplitted = self._itemPath.relativePath.split(';')
      if len(nodeIdSplitted) != 2:
        raise Exception('Invalid nodeId format')
      matches = [x for x in nodeIdSplitted if x.startswith('i=')]
      if len(matches) != 1:
        raise Exception('Invalid nodeId type')

      objectIdentity = int(matches[0][2:])
      SignatureLSB = 0xFE;
      SignatureMSB = 0xCA;

      ret = [ 0 ] * 8

      ret[0] = ((propertyIdentity & 0x000000FF) >> (0 * 8));
      ret[1] = ((propertyIdentity & 0x0000FF00) >> (1 * 8));
      ret[2] = ((objectIdentity   & 0x000000FF) >> (0 * 8));
      ret[3] = ((objectIdentity   & 0x0000FF00) >> (1 * 8));
      ret[4] = ((objectIdentity   & 0x00FF0000) >> (2 * 8));
      ret[5] = ((objectIdentity   & 0xFF000000) >> (3 * 8));
      ret[6] = SignatureLSB;
      ret[7] = SignatureMSB;

      import base64

      return 'ns=1;b=' + base64.b64encode(bytes(ret)).decode("utf-8") 




