"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import datetime as dt
import requests
import json
from .autostarttimer import AutoStartTimer

from .epmconnectioncontext import EpmConnectionContext

class AuthorizationService(object):

  def __init__(self, connectionContext, forceConnection = True):
    import copy
    self._context = copy.deepcopy(connectionContext)
    self._context += self.changedToken
    self._error = ''
    self._expireIn = 0
    self._session = None
    self._timer = None
    if forceConnection:
      self._context.setToken(self.renewToken())
      self._timer = AutoStartTimer(60, self.reloadToken)

  def reloadToken(self):
    try:
      self._context.setToken(self.renewToken())
      self._error = ''
    except Exception as ex:
      self._context.setToken('')
      self._error = str(ex)
    
  def renewToken(self):
    from datetime import datetime, timedelta

    import logging
    try:
      if (self._context.hasToken()):
       return self.refreshToken()
    except Exception as ex:
      logging.error('Refresh failed! Trying to connect again. Error: ' + str(ex))

    client_auth = requests.auth.HTTPBasicAuth(self._context.getClientId(), self._context.getProgramId())
    post_data = {"grant_type": "password", 
                  "username": self._context.getUserName(),
                  "password": self._context.getPassword(),
                  "scope": "offline_access openid profile email opcua_browse opcua_read opcua_write opcua_subscription opcua_history EpmWebApi portal_files portal_upload"} #EpmProcessor #openid profile email opcua_browse opcua_read opcua_subscription 
    auth_url = self._context.getAuthServer() + '/connect/token'

    session = self.getSession()
    response = session.post(auth_url,
                             auth=client_auth,
                             data=post_data, verify=False)
    respose_json = response.json()

    if response.status_code != 200:
        raise Exception("GetToken() call http error '" +  str(response.status_code) + "'. Reason: " + respose_json["error"])
    
    self._expireIn = respose_json["expires_in"]

    from datetime import datetime, timedelta
    self._context.setExpiration(datetime.utcnow() + timedelta(seconds=self._expireIn))
    self._context.setRefreshToken(respose_json["refresh_token"])

    return respose_json["access_token"]

  def changedToken(self, token):
    session = self.getSession()
    if token != None:
      header = {'Authorization': 'Bearer {}'.format(token)}
      session.headers.update(header)
    else:
      header = {}
      session.headers.update(header)

  def getToken(self):
    if self._error == '':
      return self._context.getToken()
    else:
      raise Exception(self._error)

  def getSession(self):
    if self._session == None:
      self._session = requests.session()
    return self._session

  def refreshToken(self):

    import logging
    from datetime import datetime, timedelta
    # agora sempre faz um refresh pra verificar a conexão
    #if (self._tokenExpiration != None and self._tokenExpiration  > (datetime.utcnow() + timedelta(seconds=60))):
    #  return self._token
    if (self._context.hasExpiration() and self._context.getExpiration() < (datetime.utcnow() + timedelta(seconds=30))):
      # tenta fechar o token
      self.close()
      raise Exception('refresh Token expired!') 

    client_auth = requests.auth.HTTPBasicAuth(self._context.getClientId(), self._context.getProgramId())
    post_data = {"grant_type": "refresh_token", 
                 "refresh_token": "%s"%(self._context.getRefreshToken()) }
    auth_url = self._context.getAuthServer() + '/connect/token'

    session = self.getSession()
    response = session.post(auth_url,
                              auth=client_auth,
                              data=post_data, verify=False) 
    respose_json = response.json()

    if response.status_code != 200:
      raise Exception("RefreshToken() call http error '" +  str(response.status_code) + "'.")

    from datetime import datetime, timedelta

    expireIn = self._expireIn
    if expireIn is None or expireIn < 60:
      expireIn = 300

    self._context.setRefreshToken(respose_json["refresh_token"])
    self._context.setExpiration(datetime.utcnow() + timedelta(seconds=expireIn))

    return respose_json["access_token"]

  def logout(self):
    if (not self._context.hasToken()):
      return
    post_data = { "token" : self._context.getToken() }
    client_auth = requests.auth.HTTPBasicAuth(self._context.getClientId(), self._context.getProgramId())
    auth_url = self._context.getAuthServer() + '/connect/revocation'
    session = self.getSession()
    response = session.post(auth_url,
                              auth=client_auth,
                              data=post_data, verify=False)
    if (not self._context.hasRefreshToken()):
      return
    post_data = { "token" : self._context.getRefreshToken(), "token_type_hint" : "refresh_token" }
    client_auth = requests.auth.HTTPBasicAuth(self._context.getClientId(), self._context.getProgramId())
    auth_url = self._context.getAuthServer() + '/connect/revocation'
    session = self.getSession()
    response = session.post(auth_url,
                              auth=client_auth,
                              data=post_data, verify=False)

  def detach(self):
    try:
      if not self._timer is None:
        self._timer.cancel()
    except Exception as ex:
      import logging
      logging.exception(ex)

    import copy
    context = copy.deepcopy(self._context)
    self._context.reset()
    return context


  def close(self):
    try:
      if self._timer != None:
        self._timer.cancel()
    except Exception as ex:
      import logging
      logging.exception(ex)
    self._context -= self.changedToken
    self.logout()

  def restart(self):
    self._context.setRefreshToken(None)
    self._context.setExpiration(None)
    self._context.setToken(None)
    self._context.setToken(self.renewToken())
    self._timer = AutoStartTimer(60, self.reloadToken)



