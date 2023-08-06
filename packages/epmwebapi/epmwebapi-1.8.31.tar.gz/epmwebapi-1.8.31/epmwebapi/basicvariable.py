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
from .epmproperty import EpmProperty
from .dataobjectattributes import DataObjectAttributes
from .epmnodeids import EpmNodeIds
from .epmdataobject import EpmDataObject, ClampingMode
from .basicvariablepropertymask import BasicVariablePropertyMask
from .historyupdatetype import HistoryUpdateType

from enum import Enum

class TagType(Enum):
    SourceType = 0

    Bit = 1

    Int = 2

    UInt = 3

    Float = 4

    Double = 5

    String = 6

    DateTime = 8

class DataTypeId(Enum):
    SourceType = None

    Bit = 1

    Int = 8

    UInt = 9

    Float = 10

    Double = 11

    String = 12

    DateTime = 13

class BasicVariable(EpmDataObject):
    """description of class"""

    def __init__(self, epmConnection, itemPath, name, description = None, tagType = None, realTimeEnabled = None, deadBandFilter = None, 
                 deadBandUnit = None, eu = None, lowLimit = None, highLimit = None, scaleEnable = None, inputLowLimit = None, 
                 inputHighLimit = None, clamping = None, domain = None, interface = None, ioTagAddress = None, processingEnabled = None, 
                 isRecording = None, isCompressing = None, storeMillisecondsEnabled = None, storageSet = None, active = None):
        super().__init__(epmConnection, name, itemPath)
        self._name = name
        self._newName = None
        self._description = description
        self._tagType = TagType.SourceType.value if tagType == None else TagType[tagType].value if isinstance(tagType, str) else tagType if isinstance(tagType, int) or tagType is None else tagType.value
        self._realTimeEnabled = realTimeEnabled
        self._deadBandFilter = deadBandFilter
        self._deadBandUnit = deadBandUnit
        self._eu = eu
        self._lowLimit = lowLimit
        self._highLimit = highLimit
        self._scaleEnable = scaleEnable
        self._inputLowLimit = inputLowLimit
        self._inputHighLimit = inputHighLimit
        self._clamping = clamping if isinstance(clamping, int) or clamping is None else clamping.value
        self._domain = domain
        self._interface = interface
        self._ioTagAddress = ioTagAddress
        self._processingEnabled = processingEnabled
        self._isRecording = isRecording
        self._isCompressing = isCompressing
        self._storeMillisecondsEnabled = storeMillisecondsEnabled
        self._storageSet = storageSet
        self._active = active

    @property
    def name(self):
      return self._name

    @name.setter
    def name(self, value):
      if self._name == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.Name.value
      self._newName = value

    @property
    def tagType(self):
      return TagType(self._tagType) if self._tagType is not None else None

    @tagType.setter
    def tagType(self, value):
      if isinstance(value, int) or value is None:
        if self._tagType == value:
          return
        self._tagType = value
      else:
        if self._tagType == value.value:
          return
        self._tagType = value.value
      self._changeMask = self._changeMask | BasicVariablePropertyMask.TagType.value

    @property
    def realTimeEnabled(self):
      return self._realTimeEnabled

    @realTimeEnabled.setter
    def realTimeEnabled(self, value):
      if self._realTimeEnabled == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.RealTimeEnabled.value
      self._realTimeEnabled = value

    @property
    def deadBandFilter(self):
      return self._deadBandFilter

    @deadBandFilter.setter
    def deadBandFilter(self, value):
      if self._deadBandFilter == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.DeadBandFilter.value
      self._deadBandFilter = value
        
    @property
    def deadBandUnit(self):
      return self._deadBandUnit

    @deadBandUnit.setter
    def deadBandUnit(self, value):
      if self._deadBandUnit == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.DeadBandUnit.value
      self._deadBandUnit = value

    @property
    def scaleEnable(self):
      return self._scaleEnable

    @scaleEnable.setter
    def scaleEnable(self, value):
      if self._scaleEnable == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.ScaleEnable.value
      self._scaleEnable = value

    @property
    def inputLowLimit(self):
      return self._inputLowLimit

    @inputLowLimit.setter
    def inputLowLimit(self, value):
      if self._inputLowLimit == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.InputLowLimit.value
      self._inputLowLimit = value
        
    @property
    def inputHighLimit(self):
      return self._inputHighLimit

    @inputHighLimit.setter
    def inputHighLimit(self, value):
      if self._inputHighLimit == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.InputHighLimit.value
      self._inputHighLimit = value
        
    @property
    def interface(self):
      return self._interface

    @interface.setter
    def interface(self, value):
      if self._interface == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.Interface.value
      self._interface = value
        
    @property
    def ioTagAddress(self):
      return self._ioTagAddress

    @ioTagAddress.setter
    def ioTagAddress(self, value):
      if self._ioTagAddress == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.IoTagAddress.value
      self._ioTagAddress = value
        
    @property
    def processingEnabled(self):
      return self._processingEnabled

    @processingEnabled.setter
    def processingEnabled(self, value):
      if self._processingEnabled == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.ProcessingEnabled.value
      self._processingEnabled = value
        
    @property
    def isRecording(self):
      return self._isRecording

    @isRecording.setter
    def isRecording(self, value):
      if self._isRecording == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.IsRecording.value
      self._isRecording = value
        
    @property
    def isCompressing(self):
      return self._isCompressing

    @isCompressing.setter
    def isCompressing(self, value):
      if self._isCompressing == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.IsCompressing.value
      self._isCompressing = value
        
    @property
    def storeMillisecondsEnabled(self):
      return self._storeMillisecondsEnabled 

    @storeMillisecondsEnabled.setter
    def storeMillisecondsEnabled(self, value):
      if self._storeMillisecondsEnabled == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.StoreMillisecondsEnabled.value
      self._storeMillisecondsEnabled = value
        
    @property
    def storageSet(self):
      return self._storageSet

    @storageSet.setter
    def storageSet(self, value):
      if self._storageSet == value:
        return
      self._changeMask = self._changeMask | BasicVariablePropertyMask.StorageSet.value
      self._storageSet = value


    #Public Methods

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
      elif attributeId == DataObjectAttributes.TagType:
        self._tagType = value

    def historyReadRaw(self, queryPeriod, bounds = False):
        if self.tagType != None and self.tagType != TagType.SourceType:
            if self._hasFlag(BasicVariablePropertyMask.TagType):
                raise Exception("Save the basic variable new tagType before writing a value")
            dataType = DataTypeId[self.tagType.name].value
            return self._epmConnection._historyReadRaw(queryPeriod, self._itemPath, bounds, "i=" + str(dataType))
        else:
            return self._epmConnection._historyReadRaw(queryPeriod, self._itemPath, bounds)

    def write(self, value, timestamp=dt.datetime.now(dt.timezone.utc), quality=0):
        if self.tagType != None and self.tagType != TagType.SourceType:
            if self._hasFlag(BasicVariablePropertyMask.TagType):
                raise Exception("Save the basic variable new tagType before writing a value")
            dataType = DataTypeId[self.tagType.name].value
            return self._epmConnection._write([self._itemPath], [13], [DataValueJSON(value, quality, timestamp,
                                                                                     dataTypeId="i="+str(dataType))])
        else:
          return self._epmConnection._write([self._itemPath], [13], [DataValueJSON(value, quality, timestamp)])

    def historyUpdate(self, values):
        if self.tagType != None and self.tagType != TagType.SourceType:
            if self._hasFlag(BasicVariablePropertyMask.TagType):
                raise Exception("Save the basic variable new tagType before using historyUpdate")
            dataType = DataTypeId[self.tagType.name].value
            return self._epmConnection._historyUpdate(HistoryUpdateType.Update.value, [ self._itemPath ], [ values ],
                                                      dataTypeId="i="+str(dataType))
        else:
            return self._epmConnection._historyUpdate(HistoryUpdateType.Update.value, [ self._itemPath ], [ values ])


    def save(self):
      self._epmConnection.updateBasicVariable(self._name, 
                                              self._newName if self._hasFlag(BasicVariablePropertyMask.Name) else None,
                                              self._description if self._hasFlag(BasicVariablePropertyMask.Description) else None,
                                              self._tagType if self._hasFlag(BasicVariablePropertyMask.TagType) else None,
                                              self._realTimeEnabled if self._hasFlag(BasicVariablePropertyMask.RealTimeEnabled) else None,
                                              self._deadBandFilter if self._hasFlag(BasicVariablePropertyMask.DeadBandFilter) else None,
                                              self._deadBandUnit if self._hasFlag(BasicVariablePropertyMask.DeadBandUnit) else None,
                                              self._eu if self._hasFlag(BasicVariablePropertyMask.Eu) else None,
                                              self._lowLimit if self._hasFlag(BasicVariablePropertyMask.LowLimit) else None,
                                              self._highLimit if self._hasFlag(BasicVariablePropertyMask.HighLimit) else None,
                                              self._scaleEnable if self._hasFlag(BasicVariablePropertyMask.ScaleEnable) else None,
                                              self._inputLowLimit if self._hasFlag(BasicVariablePropertyMask.InputLowLimit) else None,
                                              self._inputHighLimit if self._hasFlag(BasicVariablePropertyMask.InputHighLimit) else None,
                                              self._clamping if self._hasFlag(BasicVariablePropertyMask.Clamping) else None,
                                              self._domain if self._hasFlag(BasicVariablePropertyMask.Domain) else None,
                                              self._interface if self._hasFlag(BasicVariablePropertyMask.Interface) else None,
                                              self._ioTagAddress if self._hasFlag(BasicVariablePropertyMask.IoTagAddress) else None,
                                              self._processingEnabled if self._hasFlag(BasicVariablePropertyMask.ProcessingEnabled) else None,
                                              self._isRecording if self._hasFlag(BasicVariablePropertyMask.IsRecording) else None,
                                              self._isCompressing if self._hasFlag(BasicVariablePropertyMask.IsCompressing) else None,
                                              self._storeMillisecondsEnabled if self._hasFlag(BasicVariablePropertyMask.StoreMillisecondsEnabled) else None,
                                              self._storageSet if self._hasFlag(BasicVariablePropertyMask.StorageSet) else None)

      if (self._newName != None and self._hasFlag(BasicVariablePropertyMask.Name)):
        self._name = self._newName

      self._changeMask = BasicVariablePropertyMask.Unspecified.value

      


    def copy(self, newName, description = None, tagType = None, realTimeEnabled = None, deadBandFilter = None, 
            deadBandUnit = None, eu = None, lowLimit = None, highLimit = None, scaleEnable = None, inputLowLimit = None, 
            inputHighLimit = None, clamping = None, domain = None, interface = None, ioTagAddress = None, processingEnabled = None, 
            isRecording = None, isCompressing = None, storeMillisecondsEnabled = None, storageSet = None):
      return self._epmConnection.createBasicVariable(newName,
                                              description = description if description != None else self._description,
                                              tagType = tagType if tagType != None else self._tagType,
                                              realTimeEnabled = realTimeEnabled if realTimeEnabled != None else self._realTimeEnabled,
                                              deadBandFilter = deadBandFilter if deadBandFilter != None else self._deadBandFilter,
                                              deadBandUnit = deadBandUnit if deadBandUnit != None else self._deadBandUnit,
                                              eu = eu if eu != None else self._eu,
                                              lowLimit = lowLimit if lowLimit != None else self._lowLimit,
                                              highLimit = highLimit if highLimit != None else self._highLimit,
                                              scaleEnable = scaleEnable if scaleEnable != None else self._scaleEnable,
                                              inputLowLimit = inputLowLimit if inputLowLimit != None else self._inputLowLimit,
                                              inputHighLimit = inputHighLimit if inputHighLimit != None else self._inputHighLimit,
                                              clamping = clamping if clamping != None else self._clamping,
                                              domain = domain if domain != None else self._domain,
                                              interface = interface if interface != None else self._interface,
                                              ioTagAddress = ioTagAddress if ioTagAddress != None else self._ioTagAddress,
                                              processingEnabled = processingEnabled if processingEnabled != None else self._processingEnabled,
                                              isRecording = isRecording if isRecording != None else self._isRecording,
                                              isCompressing = isCompressing if isCompressing != None else self._isCompressing,
                                              storeMillisecondsEnabled = storeMillisecondsEnabled if storeMillisecondsEnabled != None else self._storeMillisecondsEnabled,
                                              storageSet = storageSet if storageSet != None else self._storageSet)

    def delete(self):
      result = self._epmConnection.deleteBasicVariable([ self._name ])
      return result[0]

    def _hasFlag(self, flag):
      return self._changeMask & flag.value == flag.value




class BasicVariableAlreadyExistsException(Exception):
    pass

class BasicVariableInvalidNameException(Exception):
    pass

class StorageSetDoesNotExistException(Exception):
    pass

class InterfaceDoesNotExistException(Exception):
    pass

