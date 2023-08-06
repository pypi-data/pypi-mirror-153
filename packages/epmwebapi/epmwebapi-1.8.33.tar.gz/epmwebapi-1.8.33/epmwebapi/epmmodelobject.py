"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from .epmobject import EpmObject

class EpmModelObject(EpmObject):
    """description of class"""

    def __init__(self, epmConnection, itemPath, path, name, type = ''):
        super().__init__(epmConnection, itemPath, path, name, type)

    # Public Methods

    def addInstances(self, names, objTypes):
        splitPath = self._path.split("/")

        if splitPath[0] == "":
            addPath = "/".join(splitPath[3:])
        else:
            addPath = "/".join(splitPath[2:])

        return self._epmConnection.addInstancesEpmModel(addPath, names, objTypes)

    def removeInstance(self, name):
        splitPath = self._path.split("/")

        if splitPath[0] == "":
            removePath = "/".join(splitPath[3:]) + "/" + name
        else:
            removePath = "/".join(splitPath[2:]) + "/" + name

        if removePath[0] == "/":
            removePath = removePath[1:]

        self._epmConnection.removeInstanceEpmModel(removePath)


    def setBindedVariables(self, aliasProperties, variablesNames):
        splitPath = self._path.split("/")

        if splitPath[0] == "":
            objectPath = "/".join(splitPath[3:])
        else:
            objectPath = "/".join(splitPath[2:])

        self._epmConnection.setBindedVariables(objectPath, aliasProperties, variablesNames, True)


class ObjectDependenciesException(Exception):
    pass


class InstanceNameDuplicatedException(Exception):
    pass


class InvalidObjectNameException(Exception):
    pass


class InvalidSourceVariableException(Exception):
    pass


class InvalidObjectTypeException(Exception):
    pass


class InvalidObjectPropertyException(Exception):
    pass
