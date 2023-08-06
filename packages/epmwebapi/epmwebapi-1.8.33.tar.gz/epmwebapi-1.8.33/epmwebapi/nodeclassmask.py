"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from enum import IntFlag

class NodeClassMask(IntFlag):

    # <summary>
    # No classes are selected.
    # </summary>
    Unspecified = 0,

    #/ <summary>
    #/ The node is an object.
    #/ </summary>
    Object = 1,

    #/ <summary>
    #/ The node is a variable.
    #/ </summary>
    Variable = 2,

    #/ <summary>
    #/ The node is a method.
    #/ </summary>
    Method = 4,

    #/ <summary>
    #/ The node is an object type.
    #/ </summary>
    ObjectType = 8,

    #/ <summary>
    #/ The node is an variable type.
    #/ </summary>
    VariableType = 16,

    #/ <summary>
    #/ The node is a reference type.
    #/ </summary>
    ReferenceType = 32,

    #/ <summary>
    #/ The node is a data type.
    #/ </summary>
    DataType = 64,

    #/ <summary>
    #/ The node is a view.
    #/ </summary>
    View = 128,
