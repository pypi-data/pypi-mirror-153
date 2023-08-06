from enum import IntFlag

class BrowseDirection(IntFlag):

    # <summary>
    # No classes are selected.
    # </summary>
    Forward = 0,

    #/ <summary>
    #/ The node is an object.
    #/ </summary>
    Inverse = 1,
