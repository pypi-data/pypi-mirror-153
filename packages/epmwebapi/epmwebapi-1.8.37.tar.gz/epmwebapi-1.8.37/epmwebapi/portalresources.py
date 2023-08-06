"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from .resourcesmanager import ResourcesManager

class PortalResources(ResourcesManager):

  def __init__(self, authorizationService, webApi):
    super().__init__(authorizationService, webApi, 'resources')



    

