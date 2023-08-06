"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""
import base64
import json
import os


class CustomTypeDefinition:
    """description of class"""

    def __init__(self, epmConnection, name, icon=None, aliasProperties=None, simpleProperties=None,
                 objectProperties=None, placeHolderTypes=None):
        self._epmConnection = epmConnection
        self._name = name

        if icon:
            self._icon = icon
        else:
            self._icon = ""

        if aliasProperties:
            self._aliasProperties = aliasProperties
        else:
            self._aliasProperties = []

        if simpleProperties:
            self._simpleProperties = simpleProperties
        else:
            self._simpleProperties = []

        if objectProperties:
            self._objectProperties = objectProperties
        else:
            self._objectProperties = []

        if placeHolderTypes:
            self._placeHolderTypes = placeHolderTypes
        else:
            self._placeHolderTypes = []

    def __str__(self):
        stringDefinition = "Custom Type Definition"
        stringDefinition += "\nname: " + self._name

        if self._icon == "" or self._icon == self.defaultIcon:
            icon = "Default"
        else:
            icon = self._icon

        stringDefinition += "\nicon: " + icon

        if self._aliasProperties:
            for alias in self._aliasProperties:
                stringDefinition += "\naliasProperties[" + str(self._aliasProperties.index(alias)) + "]: " + alias

        if self._simpleProperties:
            for simple in self._simpleProperties:
                if simple.initialValue:
                    initialValue = str(simple.initialValue)
                else:
                    initialValue = "None"
                stringDefinition += "\nsimpleProperties[" + str(self._simpleProperties.index(simple)) + "]: name = " + \
                                    simple.name + ", initialValue = " + initialValue

        if self._objectProperties:
            for obj in self._objectProperties:
                stringDefinition += "\nobjectProperties[" + str(self._objectProperties.index(obj)) + "]: name = " + \
                                    obj.name + ", customType = " + obj.customType

        if self._placeHolderTypes:
            for placeHolder in self._placeHolderTypes:
                stringDefinition += "\nplaceHolderTypes[" + str(self._placeHolderTypes.index(placeHolder)) + "]: " + placeHolder

        return stringDefinition

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def aliasProperties(self):
        return self._aliasProperties

    @property
    def simpleProperties(self):
        return self._simpleProperties

    @property
    def objectProperties(self):
        return self._objectProperties

    @property
    def placeHolderTypes(self):
        return self._placeHolderTypes

    @property
    def defaultIcon(self):
        return "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7" \
               "DAcdvqGQAAAJ7SURBVDhPnVNLa1NREJ6btDdptfZhWkiELlx05cIui+5ERNwrFOxPcOUPEESK4EIQd7pxI7qptFgFH7gSt4LQFpWKAW" \
               "uSm7R53vO6c/zmJqRod174mMO5M9/MfHMmKJVK9O83f38zy6q7EAS06Nmf8rH66C19+rW6kgxchl9KsPTk/Xwxn7usmM82bbLYMO6MT" \
               "pJjbB0JvDXE2tbIuJccx+uu0X5Te3yzkxKcf7WVu1qaKp8Is7N1nVBkHNUAsfuAs5YY1jtLHjbnEeWsirXZULuV5eDcxtbMheJEvZQf" \
               "pcmRLMXMVFEgQOaadmS8p8lMQF5raseaap2YWhpkSULx1s9isLT2JXt6Oh8Xx8LRQjhCc7kROg4inTBFsaFvjRZtR01q9TQyOyJGCSB" \
               "lY1iXo/FUg4VHbytT+XBuFsGFMEulXEjGGHq+U0b/KN9YImT0DgAxoUq2ttF8PXkyI0LAOYpQ3m5P0feuoR84GzizNuQVAMu4YyVQ/X" \
               "ttq2rnOqUEEKfGiaMYve+h7K9tjYSYGERj9M4gQckpREgvwlpTkdg+gXORN1IifgANBFgZ4SAAzv3AwXlwXx0SYNZRnxVlixNIerAk/" \
               "YtwjlObAj4oHwT2kAAvbbfviB+w8ng60rcEpOKJBdIqkF18rTtswdUPHnA3/iAVSCUyrja0kGBKlQfSFiWJnOVxmc9DgsrDGz3zO7rC" \
               "ne47GZW00YUOMnOPkWEfMHqQYYQY6w6wnLSSdYn9a5kKK6vjYXH2RTAxfnEaWat70aGASm8j8A5aeHqweW+4VEe2cebarbHcfHFtNJO" \
               "5pJod4p7axgLdxlN+tr9+9+g2ejzL//+I/gCSwRoBoUN0GgAAAABJRU5ErkJggg=="

    # Public Methods

    def updateIcon(self, pathName):
        with open(pathName, "rb") as imageFile:
            icon = base64.b64encode(imageFile.read()).decode("utf-8")
            if self._icon == icon:
                return
            self._icon = icon

    def removeIcon(self):
        icon = ""
        if self._icon == icon:
            return
        self._icon = icon

    def addAliasProperty(self, aliasName):
        if len(self._aliasProperties) == 0:
            self._aliasProperties.append(aliasName)
        else:
            names = []
            for name in self._aliasProperties:
                names.append(name)

            if aliasName not in names:
                self._aliasProperties.append(aliasName)
            else:
                raise Exception("Name already exists")

    def removeAliasProperty(self, aliasName):
        names = []
        for name in self._aliasProperties:
            names.append(name)

        if aliasName in names:
            self._aliasProperties.remove(aliasName)
        else:
            raise Exception("Alias Property not found")

    def addSimpleProperty(self, simpleName, initialValue = None):
        if len(self._simpleProperties) == 0:
            newSimpleProperty = SimpleProperty(simpleName, initialValue)
        else:
            names = []
            for item in self._simpleProperties:
                names.append(item.name)
            if simpleName not in names:
                newSimpleProperty = SimpleProperty(simpleName, initialValue)
            else:
                raise Exception("Name already exists")

        self._simpleProperties.append(newSimpleProperty)

    def removeSimpleProperty(self, simpleName):
        names = []
        for item in self._simpleProperties:
            names.append(item.name)
        if simpleName in names:
            self._simpleProperties.pop(names.index(simpleName))
        else:
            raise Exception("Simple Property not found")

    def addObjectProperty(self, objectName, customType):
        if customType not in self._epmConnection.getAllCustomTypes():
            raise Exception("Object Property type does not exist")

        if len(self._objectProperties) == 0:
            newObjectProperty = ObjectProperty(objectName, customType)
        else:
            names = []
            for item in self._objectProperties:
                names.append(item.name)
            if objectName not in names:
                newObjectProperty = ObjectProperty(objectName, customType)
            else:
                raise Exception("Name already exists")

        self._objectProperties.append(newObjectProperty)

    def removeObjectProperty(self, objectName):
        names = []
        for item in self._objectProperties:
            names.append(item.name)
        if objectName in names:
            self._objectProperties.pop(names.index(objectName))
        else:
            raise Exception("Object Property not found")

    def addPlaceHolderType(self, customTypeName):
        if customTypeName in self._placeHolderTypes:
            raise Exception("Type already in a PlaceHolder")

        if customTypeName in self._epmConnection.getAllCustomTypes():
            self._placeHolderTypes.append(customTypeName)
        else:
            raise Exception("PlaceHolder type does not exist")

    def removePlaceHolderType(self, customTypeName):
        if customTypeName in self._placeHolderTypes:
            self._placeHolderTypes.remove(customTypeName)
        else:
            raise Exception("PlaceHolder not found")

    def save(self):
        self._epmConnection.updateCustomType(self.exportJSON())

    def delete(self):
        self._epmConnection.deleteCustomType(self._name)

    def exportJSON(self, fileName = None, pathName = None):
        aliasPropertiesList = []
        for aliasName in self._aliasProperties:
            aliasPropertiesList.append({'name': aliasName})

        simplePropertiesList = []
        for simpleProperty in self._simpleProperties:
            simplePropertiesList.append({'name': simpleProperty.name, 'initialValue': simpleProperty.initialValue})

        objectPropertiesList = []
        for objectProperty in self._objectProperties:
            objectPropertiesList.append({'name': objectProperty.name, 'type': objectProperty.customType})

        placeHolderPropertiesList = []
        for placeHolderType in self._placeHolderTypes:
            placeHolderPropertiesList.append({'type': placeHolderType})

        propertiesJSON = {'name': self.name, 'icon': self.icon, 'aliasProperties': aliasPropertiesList,
                          'simpleProperties': simplePropertiesList, 'objectProperties': objectPropertiesList,
                          'placeHolderProperties': placeHolderPropertiesList}

        if fileName is not None:
            if pathName is None:
                pathName = os.getcwd()
            fileName = fileName + '.json'
            with open(os.path.join(pathName, fileName), 'w') as outfile:
                json.dump(propertiesJSON, outfile)

        return propertiesJSON


class SimpleProperty:

    def __init__(self, name, initialValue = None):
        self._name = name
        self._initialValue = initialValue

    @property
    def name(self):
        return self._name

    @property
    def initialValue(self):
        return self._initialValue


class ObjectProperty:

    def __init__(self, name, customType):
        self._name = name
        self._customType = customType

    @property
    def name(self):
        return self._name

    @property
    def customType(self):
        return self._customType


class CustomTypeAlreadyExistsException(Exception):
    pass


class InvalidCustomTypeNameException(Exception):
    pass


class CustomTypeDependenciesException(Exception):
    pass


class InvalidIconException(Exception):
    pass


class DuplicatedPropertiesNamesException(Exception):
    pass


class DuplicatedPropertiesTypeException(Exception):
    pass


class MissingPropertyNameException(Exception):
    pass


class InvalidPropertyTypeException(Exception):
    pass


class InvalidPropertyNameException(Exception):
    pass
