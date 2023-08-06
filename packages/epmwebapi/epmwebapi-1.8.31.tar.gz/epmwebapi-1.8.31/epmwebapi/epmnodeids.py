"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from enum import Enum

class EpmNodeIds(Enum):

    HasTags = 'ns=4;i=96'

    Organizes = 'ns=0;i=35'

    HasComponent = 'ns=0;i=47'

    HasProperty = 'ns=0;i=46'

    BasicVariableType = 'ns=4;i=94'

    ExpressionVariableType = 'ns=4;i=289'

    AnnotationType = 'ns=0;i=891'

    HasTypeDefinition = 'ns=0;i=40'


