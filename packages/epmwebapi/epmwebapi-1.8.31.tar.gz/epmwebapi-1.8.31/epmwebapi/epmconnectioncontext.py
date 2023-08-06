class EpmConnectionContext(object):
    """description of class"""
    def __init__(self, authServer, webapi, clientId, programId, userName, password, token = None, refreshToken = None, expiration = None):
      self._authServer = authServer
      self._webapi = webapi
      self._clientId = clientId
      self._programId = programId
      self._userName = userName
      self._password = password
      self._token = token
      self._refreshToken = refreshToken
      self._expiration = expiration
      self._eventhandler = []

    def __iadd__(self, ehandler):
      self._eventhandler.append(ehandler) 
      return self

    def __isub__(self, ehandler):
      self._eventhandler.remove(ehandler) 
      return self

    def onchangeToken(self, token): 
      for eventhandler in self._eventhandler: 
        eventhandler(token)

    def set(self, authServer, webapi, clientId, programId, userName, password, token, refreshToken, expiration):
      self._authServer = authServer
      self._webapi = webapi
      self._clientId = clientId
      self._programId = programId
      self._userName = userName
      self._password = password
      self._token = token
      self._refreshToken = refreshToken
      self._expiration = expiration

    def reset(self):
      self._authServer = None
      self._webapi = None
      self._clientId = None
      self._programId = None
      self._userName = None
      self._password = None
      self._token = None
      self._refreshToken = None
      self._expiration = None

    def isValidToken(self):
      if self.hasExpiration():
        from datetime import datetime, timedelta
        return self._expiration < datetime.utcnow() + timedelta(seconds=10) 
      return False

    def hasToken(self):
      return self._token != None

    def hasRefreshToken(self):
      return self._refreshToken != None

    def hasExpiration(self):
      return self._expiration != None

    def getAuthServer(self):
      return self._authServer

    def setAuthServer(self, authServer):
      self._authServer = authServer

    def getWebApi(self):
      return self._webapi

    def setWebApi(self, webapi):
      self._webapi = webapi


    def getClientId(self):
      return self._clientId

    def setClientId(self, clientId):
      self._clientId = clientId

    def getProgramId(self):
      return self._programId

    def setProgramId(self, programId):
      self._programId = programId

    def getUserName(self):
      return self._userName

    def setUserName(self, userName):
      self._userName = userName

    def getPassword(self):
      return self._password

    def setPassword(self, password):
      self._password = password

    def getToken(self):
      return self._token

    def setToken(self, token):
      self._token = token
      self.onchangeToken(token)

    def getRefreshToken(self):
      return self._refreshToken

    def setRefreshToken(self, refreshToken):
      self._refreshToken = refreshToken

    def getExpiration(self):
      return self._expiration

    def setExpiration(self, expiration):
      self._expiration = expiration


