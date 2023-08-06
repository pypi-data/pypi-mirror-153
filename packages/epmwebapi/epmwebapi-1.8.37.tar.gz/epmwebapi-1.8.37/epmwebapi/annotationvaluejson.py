"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

class AnnotationValueJSON(object):
    """description of class"""
    def __init__(self, message, userName, annotationTime):
        self._message = message
        self._userName = userName
        self._annotationTime = annotationTime

    @property
    def message(self):
      return self._message

    @property
    def userName(self):
      return self._userName

    @property
    def annotationTime(self):
      return self._annotationTime

    def toDict(self):
        from .epmnodeids import EpmNodeIds
        return {'value': { 
                            'annotationTime' : self._annotationTime.isoformat(), 
                            'message' : self._message,
                            'userName' : self._userName 
                         }, 
                'quality': 0, 
                'timestamp' : self._annotationTime.isoformat(),
                'dataTypeId': EpmNodeIds.AnnotationType.value }
