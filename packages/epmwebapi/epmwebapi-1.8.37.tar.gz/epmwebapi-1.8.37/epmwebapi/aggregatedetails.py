"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from enum import Enum

class AggregateType(Enum):
    # <summary>
    # The identifier for the Trend Object.
    # </summary>
    Trend = 'Trend'

    # <summary>
    # The identifier for the Interpolative Object.
    # </summary>
    Interpolative = 'Interpolative'

    # <summary>
    # The identifier for the Average Object.
    # </summary>
    Average = 'Average'

    # <summary>
    # The identifier for the TimeAverage Object.
    # </summary>
    TimeAverage = 'TimeAverage'

    # <summary>
    # The identifier for the Total Object.
    # </summary>
    Total = 'Total'

    # <summary>
    # The identifier for the Minimum Object.
    # </summary>
    Minimum = 'Minimum'

    # <summary>
    # The identifier for the Maximum Object.
    # </summary>
    Maximum = 'Maximum'

    # <summary>
    # The identifier for the MinimumActualTime Object.
    # </summary>
    MinimumActualTime = 'MinimumActualTime'

    # <summary>
    # The identifier for the MaximumActualTime Object.
    # </summary>
    MaximumActualTime = 'MaximumActualTime'

    # <summary>
    # The identifier for the Range Object.
    # </summary>
    Range = 'Range'

    # <summary>
    # The identifier for the AnnotationCount Object.
    # </summary>
    AnnotationCount = 'AnnotationCount'

    # <summary>
    # The identifier for the Count Object.
    # </summary>
    Count = 'Count'

    # <summary>
    # The identifier for the DurationInStateZero Object.
    # </summary>
    DurationInStateZero = 'DurationInStateZero'

    # <summary>
    # The identifier for the DurationInStateNonZero Object.
    # </summary>
    DurationInStateNonZero = 'DurationInStateNonZero'

    # <summary>
    # The identifier for the PercentInStateZero Object.
    # </summary>
    PercentInStateZero = 'PercentInStateZero'

    # <summary>
    # The identifier for the PercentInStateNonZero Object.
    # </summary>
    PercentInStateNonZero = 'PercentInStateNonZero'

    # <summary>
    # The identifier for the NumberOfTransitions Object.
    # </summary>
    NumberOfTransitions = 'NumberOfTransitions'

    # <summary>
    # The identifier for the Start Object.
    # </summary>
    Start = 'Start'

    # <summary>
    # The identifier for the End Object.
    # </summary>
    End = 'End'

    # <summary>
    # The identifier for the Delta Object.
    # </summary>
    Delta = 'Delta'

    # <summary>
    # The identifier for the DurationGood Object.
    # </summary>
    DurationGood = 'DurationGood'

    # <summary>
    # The identifier for the DurationBad Object.
    # </summary>
    DurationBad = 'DurationBad'

    # <summary>
    # The identifier for the PercentGood Object.
    # </summary>
    PercentGood = 'PercentGood'

    # <summary>
    # The identifier for the PercentBad Object.
    # </summary>
    PercentBad = 'PercentBad'

    # <summary>
    # The identifier for the WorstQuality Object.
    # </summary>
    WorstQuality = 'WorstQuality'

    # <summary>
    # The identifier for the TimeAverage2 Object.
    # </summary>
    TimeAverage2 = 'TimeAverage2'

    # <summary>
    # The identifier for the Total2 Object.
    # </summary>
    Total2 = 'Total2'

    # <summary>
    # The identifier for the Minimum2 Object.
    # </summary>
    Minimum2 = 'Minimum2'

    # <summary>
    # The identifier for the Maximum2 Object.
    # </summary>
    Maximum2 = 'Maximum2'

    # <summary>
    # The identifier for the MinimumActualTime2 Object.
    # </summary>
    MinimumActualTime2 = 'MinimumActualTime2'

    # <summary>
    # The identifier for the MaximumActualTime2 Object.
    # </summary>
    MaximumActualTime2 = 'MaximumActualTime2'

    # <summary>
    # The identifier for the Range2 Object.
    # </summary>
    Range2 = 'Range2'

    # <summary>
    # The identifier for the StartBounds Object.
    # </summary>
    StartBound = 'StartBound'

    # <summary>
    # The identifier for the EndBounds Object.
    # </summary>
    EndBound = 'EndBound'

    # <summary>
    # The identifier for the DeltaBounds Object.
    # </summary>
    DeltaBounds = 'DeltaBounds'

    # <summary>
    # The identifier for the WorstQuality2 Object.
    # </summary>
    WorstQuality2 = 'WorstQuality2'

    # <summary>
    # The identifier for the StandardDeviationPopulation Object.
    # </summary>
    StandardDeviationPopulation = 'StandardDeviationPopulation'

    # <summary>
    # The identifier for the VariancePopulation Object.
    # </summary>
    VariancePopulation = 'VariancePopulation'

    # <summary>
    # The identifier for the StandardDeviationSample Object.
    # </summary>
    StandardDeviationSample = 'StandardDeviationSample'

    # <summary>
    # The identifier for the VarianceSample Object.
    # </summary>
    VarianceSample = 'VarianceSample'

class AggregateDetails(object):
    """description of class"""

    def __init__(self, interval, type):
        self._interval = interval
        self._type = type.value

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
