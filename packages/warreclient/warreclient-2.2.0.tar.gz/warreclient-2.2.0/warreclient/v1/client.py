#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from warreclient import client
from warreclient import exceptions
from warreclient.v1 import flavorprojects
from warreclient.v1 import flavors
from warreclient.v1 import limits
from warreclient.v1 import reservations


class Client(object):
    """Client for Warre v1 API
    :param string session: session
    :type session: :py:class:`keystoneauth.adapter.Adapter`
    """

    def __init__(self, session=None, service_type='nectar-reservation',
                 **kwargs):
        """Initialize a new client for the Warre v1 API."""
        if session is None:
            raise exceptions.ClientException(
                message='Session is required argument')
        self.http_client = client.SessionClient(
            session, service_type=service_type, **kwargs)
        self.flavorprojects = flavorprojects.FlavorProjectManager(
            self.http_client)
        self.flavors = flavors.FlavorManager(self.http_client)
        self.limits = limits.LimitsManager(self.http_client)
        self.reservations = reservations.ReservationManager(self.http_client)
