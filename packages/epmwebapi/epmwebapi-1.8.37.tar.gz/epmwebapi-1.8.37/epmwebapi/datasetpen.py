"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import datetime
import re
from datetime import timedelta

from .aggregatedetails import AggregateType, AggregateDetails
from .itempathjson import ItemPathJSON
from .nodeattributes import NodeAttributes


class DatasetPen(object):
    """description of class"""
    def __init__(self, dataset, title, dataSourceName = None, penConfig = None):
        import clr
        self._dataset = dataset
        self._aggregateType = None
        self._dataSource = None
        if penConfig is None:
            self.setTitle(title)
            self._isRaw = True
            if dataSourceName is not None:
                self.setDataSource(dataSourceName)
        else:
            self._title = title
            self._penConfig = penConfig
            import os
            import clr
            clr.AddReference(os.path.dirname(os.path.abspath(__file__)) + '/dll_references/EpmData')
            from Elipse.Epm.Common import RawByPeriod, TrendMode, DatasetField
            if not isinstance(penConfig, DatasetField):
                raise Exception("Invalid penConfig")
            nsInfo = penConfig.Identity.NamespaceIndex
            nodeId = penConfig.Identity.Numeric32Identifier
            identity = 'ns=' + str(nsInfo) + ';i=' + str(nodeId)
            itemPath = ItemPathJSON('OPCUA.NodeId', None, identity)
            result = dataset._connection._read([itemPath], [NodeAttributes.BrowseName.value] * len([itemPath])).items()
            dataSourceName = result[0][0].value.value['name']
            self.setDataSource(dataSourceName)
            if isinstance(penConfig.Mode, RawByPeriod):
                self._isRaw = True
                self._aggregateType = None
            else:
                self._isRaw = False
                if isinstance(penConfig.Mode, TrendMode):
                    self._getAggregateType(1, penConfig.Mode.SampleInterval.TotalMilliseconds)
                else:
                    self._getAggregateType(penConfig.Mode.CalculateType, penConfig.Mode.SampleInterval.TotalMilliseconds)


    @property
    def title(self):
        return self._title

    @property
    def dataSource(self):
        return self._dataSource

    @property
    def isRaw(self):
      return self._isRaw

    @property
    def aggregateType(self):
      return self._aggregateType

    def setTitle(self, title):
        if type(title) is str:
            if len(title) > self._dataset.NAME_MAX_SIZE:
                raise Exception("Title cannot exceed " + str(self._dataset.NAME_MAX_SIZE) + " characters")
            elif re.search(self._dataset.REGEX_PATTERN, title):
                raise Exception("Invalid character on string argument")
            else:
                self._title = title
        else:
            raise Exception("Argument must be a string")

    def setAggregationType(self, aggregateType, processInterval):
        if not isinstance(aggregateType, AggregateType):
            raise Exception("aggregateType argument must be of type AggregateType")
        if not isinstance(processInterval, datetime.timedelta):
            raise Exception("processInterval argument must be of type timedelta")
        self._aggregateType = AggregateDetails(processInterval, aggregateType)
        self._isRaw = False

    def setRawType(self):
        self._isRaw = True

    def setDataSource(self, name):
        self._dataSource = self._dataset._connection.getDataObjects(name)[name]

    def _getAggregateType(self, aggregateId, processInterval):
        import os
        import clr
        clr.AddReference(os.path.dirname(os.path.abspath(__file__)) + '/dll_references/EpmData')
        from Elipse.Epm.Common import AggregateType as at
        if aggregateId == at.Trend:
            aggregateType = AggregateType.Trend
        elif aggregateId == at.Interpolative:
            aggregateType = AggregateType.Interpolative
        elif aggregateId == at.Average:
            aggregateType = AggregateType.Average
        elif aggregateId == at.Total:
            aggregateType = AggregateType.Total
        elif aggregateId == at.Count:
            aggregateType = AggregateType.Count
        elif aggregateId == at.Minimum:
            aggregateType = AggregateType.Minimum
        elif aggregateId == at.Maximum:
            aggregateType = AggregateType.Maximum
        elif aggregateId == at.MinimumActualTime:
            aggregateType = AggregateType.MinimumActualTime
        elif aggregateId == at.MaximumActualTime:
            aggregateType = AggregateType.MaximumActualTime
        elif aggregateId == at.Range:
            aggregateType = AggregateType.Range
        elif aggregateId == at.Delta:
            aggregateType = AggregateType.Delta
        elif aggregateId == at.TimeAverage:
            aggregateType = AggregateType.TimeAverage
        elif aggregateId == at.AnnotationCount:
            aggregateType = AggregateType.AnnotationCount
        elif aggregateId == at.DurationInStateZero:
            aggregateType = AggregateType.DurationInStateZero
        elif aggregateId == at.DurationInStateNonZero:
            aggregateType = AggregateType.DurationInStateNonZero
        elif aggregateId == at.NumberOfTransitions:
            aggregateType = AggregateType.NumberOfTransitions
        elif aggregateId == at.Start:
            aggregateType = AggregateType.Start
        elif aggregateId == at.End:
            aggregateType = AggregateType.End
        elif aggregateId == at.DurationGood:
            aggregateType = AggregateType.DurationGood
        elif aggregateId == at.DurationBad:
            aggregateType = AggregateType.DurationBad
        elif aggregateId == at.PercentGood:
            aggregateType = AggregateType.PercentGood
        elif aggregateId == at.PercentBad:
            aggregateType = AggregateType.PercentBad
        elif aggregateId == at.WorstQuality:
            aggregateType = AggregateType.WorstQuality
        elif aggregateId == at.PercentInStateZero:
            aggregateType = AggregateType.PercentInStateZero
        elif aggregateId == at.PercentInStateNonZero:
            aggregateType = AggregateType.PercentInStateNonZero
        elif aggregateId == at.TimeAverage2:
            aggregateType = AggregateType.TimeAverage2
        elif aggregateId == at.Total2:
            aggregateType = AggregateType.Total2
        elif aggregateId == at.Minimum2:
            aggregateType = AggregateType.Minimum2
        elif aggregateId == at.Maximum2:
            aggregateType = AggregateType.Maximum2
        elif aggregateId == at.MinimumActualTime2:
            aggregateType = AggregateType.MinimumActualTime2
        elif aggregateId == at.MaximumActualTime2:
            aggregateType = AggregateType.MaximumActualTime2
        elif aggregateId == at.Range2:
            aggregateType = AggregateType.Range2
        elif aggregateId == at.StartBounds:
            aggregateType = AggregateType.StartBound
        elif aggregateId == at.EndBounds:
            aggregateType = AggregateType.EndBound
        elif aggregateId == at.DeltaBounds:
            aggregateType = AggregateType.DeltaBounds
        elif aggregateId == at.WorstQuality2:
            aggregateType = AggregateType.WorstQuality2
        elif aggregateId == at.StandardDeviationPopulation:
            aggregateType = AggregateType.StandardDeviationPopulation
        elif aggregateId == at.VariancePopulation:
            aggregateType = AggregateType.VariancePopulation
        elif aggregateId == at.StandardDeviationSample:
            aggregateType = AggregateType.StandardDeviationSample
        elif aggregateId == at.VarianceSample:
            aggregateType = AggregateType.VarianceSample
        else:
            raise Exception("Aggregation type error")

        processInterval = timedelta(milliseconds=processInterval)

        self._aggregateType = AggregateDetails(processInterval, aggregateType)

    def _getAggregateId(self):
        import os
        import clr
        clr.AddReference(os.path.dirname(os.path.abspath(__file__)) + '/dll_references/EpmData')
        from Elipse.Epm.Common import AggregateType as at
        aggregateType = self.aggregateType.type
        if aggregateType == AggregateType.Trend.name:
            aggregateId = at.Trend
        elif aggregateType == AggregateType.Interpolative.name:
            aggregateId = at.Interpolative
        elif aggregateType == AggregateType.Average.name:
            aggregateId = at.Average
        elif aggregateType == AggregateType.Total.name:
            aggregateId = at.Total
        elif aggregateType == AggregateType.Count.name:
            aggregateId = at.Count
        elif aggregateType == AggregateType.Minimum.name:
            aggregateId = at.Minimum
        elif aggregateType == AggregateType.Maximum.name:
            aggregateId = at.Maximum
        elif aggregateType == AggregateType.MinimumActualTime.name:
            aggregateId = at.MinimumActualTime
        elif aggregateType == AggregateType.MaximumActualTime.name:
            aggregateId = at.MaximumActualTime
        elif aggregateType == AggregateType.Range.name:
            aggregateId = at.Range
        elif aggregateType == AggregateType.Delta.name:
            aggregateId = at.Delta
        elif aggregateType == AggregateType.TimeAverage.name:
            aggregateId = at.TimeAverage
        elif aggregateType == AggregateType.AnnotationCount.name:
            aggregateId = at.AnnotationCount
        elif aggregateType == AggregateType.DurationInStateZero.name:
            aggregateId = at.DurationInStateZero
        elif aggregateType == AggregateType.DurationInStateNonZero.name:
            aggregateId = at.DurationInStateNonZero
        elif aggregateType == AggregateType.NumberOfTransitions.name:
            aggregateId = at.NumberOfTransitions
        elif aggregateType == AggregateType.Start.name:
            aggregateId = at.Start
        elif aggregateType == AggregateType.End.name:
            aggregateId = at.End
        elif aggregateType == AggregateType.DurationGood.name:
            aggregateId = at.DurationGood
        elif aggregateType == AggregateType.DurationBad.name:
            aggregateId = at.DurationBad
        elif aggregateType == AggregateType.PercentGood.name:
            aggregateId = at.PercentGood
        elif aggregateType == AggregateType.PercentBad.name:
            aggregateId = at.PercentBad
        elif aggregateType == AggregateType.WorstQuality.name:
            aggregateId = at.WorstQuality
        elif aggregateType == AggregateType.PercentInStateZero.name:
            aggregateId = at.PercentInStateZero
        elif aggregateType == AggregateType.PercentInStateNonZero.name:
            aggregateId = at.PercentInStateNonZero
        elif aggregateType == AggregateType.TimeAverage2.name:
            aggregateId = at.TimeAverage2
        elif aggregateType == AggregateType.Total2.name:
            aggregateId = at.Total2
        elif aggregateType == AggregateType.Minimum2.name:
            aggregateId = at.Minimum2
        elif aggregateType == AggregateType.Maximum2.name:
            aggregateId = at.Maximum2
        elif aggregateType == AggregateType.MinimumActualTime2.name:
            aggregateId = at.MinimumActualTime2
        elif aggregateType == AggregateType.MaximumActualTime2.name:
            aggregateId = at.MaximumActualTime2
        elif aggregateType == AggregateType.Range2.name:
            aggregateId = at.Range2
        elif aggregateType == AggregateType.StartBound.name:
            aggregateId = at.StartBounds
        elif aggregateType == AggregateType.EndBound.name:
            aggregateId = at.EndBounds
        elif aggregateType == AggregateType.DeltaBounds.name:
            aggregateId = at.DeltaBounds
        elif aggregateType == AggregateType.WorstQuality2.name:
            aggregateId = at.WorstQuality2
        elif aggregateType == AggregateType.StandardDeviationPopulation.name:
            aggregateId = at.StandardDeviationPopulation
        elif aggregateType == AggregateType.VariancePopulation.name:
            aggregateId = at.VariancePopulation
        elif aggregateType == AggregateType.StandardDeviationSample.name:
            aggregateId = at.StandardDeviationSample
        elif aggregateType == AggregateType.VarianceSample.name:
            aggregateId = at.VarianceSample
        else:
            raise Exception("Aggregation type error")

        return aggregateId
