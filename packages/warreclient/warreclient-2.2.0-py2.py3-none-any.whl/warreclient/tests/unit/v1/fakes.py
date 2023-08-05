#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import re

try:
    from unittest import mock
except ImportError:
    import mock

from six.moves.urllib import parse

from warreclient import client as base_client
from warreclient.tests.unit import fakes
from warreclient.tests.unit import utils
from warreclient.v1 import client
from warreclient.v1 import flavorprojects
from warreclient.v1 import flavors
from warreclient.v1 import limits
from warreclient.v1 import reservations


# regex to compare callback to result of get_endpoint()
# checks version number (vX or vX.X where X is a number)
# and also checks if the id is on the end
ENDPOINT_RE = re.compile(
    r"^get_http:__warre_api:8774_v\d(_\d)?_\w{32}$")

# accepts formats like v2 or v2.1
ENDPOINT_TYPE_RE = re.compile(r"^v\d(\.\d)?$")

# accepts formats like v2 or v2_1
CALLBACK_RE = re.compile(r"^get_http:__warre_api:8774_v\d(_\d)?$")

generic_flavor = {
    "name": "s2.small",
    "id": "d6506b62-13c2-4dec-a556-b306bb5e959f",
    "max_length_hours": 24,
    "properties": "gpu=v100",
    "vcpu": 1,
    "slots": 1,
    "memory_mb": 4096,
    "is_public": True,
    "disk_gb": 30,
    "active": True,
    "description": "Desc 2",
    "extra_specs": {},
    "end": "2021-04-04T01:00:00",
    "start": "2021-04-04T00:00:00",
}

generic_flavorproject = {
    "id": "b719aadd-9340-40e9-88d0-702836c6f592",
    "project_id": "9427903ca1544f0795ba4117d55ed9b2",
    "flavor": "987d558c-3ac3-4bc0-962a-aeb1fbebf5bb",
}

generic_reservation = {
    "user_id": "c0645ff94b864d3d84c438d9855f9cea",
    "id": "17664847-0aa0-4a2b-9fe4-073b922914e5",
    "lease_id": None,
    "status": "PENDING_CREATE",
    "end": "2021-04-04T01:00:00",
    "flavor": generic_flavor,
    "project_id": "9427903ca1544f0795ba4117d55ed9b2",
    "start": "2021-04-04T00:00:00"
}

generic_limits = {
    "absolute": {
        "maxHours": 49,
        "maxReservations": 10,
        "totalHoursUsed": 27,
        "totalReservationsUsed": 4
    }
}


class FakeClient(fakes.FakeClient, client.Client):

    def __init__(self, *args, **kwargs):
        client.Client.__init__(self, session=mock.Mock())
        self.http_client = FakeSessionClient(**kwargs)
        self.flavors = flavors.FlavorManager(self.http_client)
        self.flavorprojects = flavorprojects.FlavorProjectManager(
            self.http_client)
        self.limits = limits.LimitsManager(self.http_client)
        self.reservations = reservations.ReservationManager(self.http_client)


class FakeSessionClient(base_client.SessionClient):

    def __init__(self, *args, **kwargs):

        self.callstack = []
        self.visited = []
        self.auth = mock.Mock()
        self.session = mock.Mock()
        self.service_type = 'service_type'
        self.service_name = None
        self.endpoint_override = None
        self.interface = None
        self.region_name = None
        self.version = None
        self.auth.get_auth_ref.return_value.project_id = 'tenant_id'
        # determines which endpoint to return in get_endpoint()
        # NOTE(augustina): this is a hacky workaround, ultimately
        # we need to fix our whole mocking architecture (fixtures?)
        if 'endpoint_type' in kwargs:
            self.endpoint_type = kwargs['endpoint_type']
        else:
            self.endpoint_type = 'endpoint_type'
        self.logger = mock.MagicMock()

    def request(self, url, method, **kwargs):
        return self._cs_request(url, method, **kwargs)

    def _cs_request(self, url, method, **kwargs):
        # Check that certain things are called correctly
        if method in ['GET', 'DELETE']:
            assert 'data' not in kwargs
        elif method == 'PUT':
            assert 'data' in kwargs

        if url is not None:
            # Call the method
            args = parse.parse_qsl(parse.urlparse(url)[4])
            kwargs.update(args)
            munged_url = url.rsplit('?', 1)[0]
            munged_url = munged_url.strip('/').replace('/', '_')
            munged_url = munged_url.replace('.', '_')
            munged_url = munged_url.replace('-', '_')
            munged_url = munged_url.replace(' ', '_')
            munged_url = munged_url.replace('!', '_')
            munged_url = munged_url.replace('@', '_')
            munged_url = munged_url.replace('%20', '_')
            munged_url = munged_url.replace('%3A', '_')
            callback = "%s_%s" % (method.lower(), munged_url)

        if not hasattr(self, callback):
            raise AssertionError('Called unknown API method: %s %s, '
                                 'expected fakes method name: %s' %
                                 (method, url, callback))

        # Note the call
        self.visited.append(callback)
        self.callstack.append((method, url, kwargs.get('data'),
                               kwargs.get('params')))

        status, headers, data = getattr(self, callback)(**kwargs)

        r = utils.TestResponse({
            "status_code": status,
            "text": data,
            "headers": headers,
        })
        return r, data

    def get_v1_flavors(self, **kw):
        flavors = [
            {
                "name": "s1.small",
                "id": "d4159bb0-b319-405f-89a1-5faee1596f9c",
                "max_length_hours": 24,
                "properties": None,
                "vcpu": 1,
                "slots": 1,
                "memory_mb": 4096,
                "is_public": False,
                "disk_gb": 30,
                "active": False,
                "description": "Desc 1",
                "extra_specs": {},
            },
            {
                "name": "s2.small",
                "id": "d6506b62-13c2-4dec-a556-b306bb5e959f",
                "max_length_hours": 24,
                "properties": "gpu=v100",
                "vcpu": 1,
                "slots": 1,
                "memory_mb": 4096,
                "is_public": True,
                "disk_gb": 30,
                "active": True,
                "description": "Desc 2",
                "extra_specs": {},
            }
        ]
        return (200, {}, flavors)

    def get_v1_flavors_123(self, **kw):
        return (200, {}, generic_flavor)

    def get_v1_flavors_123_freeslots(self, **kw):
        return (200, {}, [{"end": "2021-06-18T00:00:00",
                           "start": "2021-05-19T00:00:00"}])

    def patch_v1_flavors_123(self, data, **kw):
        return (202, {'slots': 2},
            {
                "name": "s2.small",
                "id": "d6506b62-13c2-4dec-a556-b306bb5e959f",
                "max_length_hours": 24,
                "properties": "gpu=v100",
                "vcpu": 1,
                "slots": 2,
                "memory_mb": 4096,
                "is_public": True,
                "disk_gb": 30,
                "active": True,
                "description": "Desc 2"
            })

    def post_v1_flavors(self, **kw):
        return (200, {}, generic_flavor)

    def delete_v1_flavors_123(self, **kw):
        return (204, {}, '')

    def get_v1_flavorprojects(self, **kw):
        flavorprojects = [
            {
                "id": "b719aadd-9340-40e9-88d0-702836c6f592",
                "project_id": "9427903ca1544f0795ba4117d55ed9b2",
                "flavor": "987d558c-3ac3-4bc0-962a-aeb1fbebf5bb",
            },
            {
                "id": "8ba07d79-8c64-4dab-926b-aaeef0fde5af",
                "project_id": "9427903ca1544f0795ba4117d55ed9b2",
                "flavor": "41c33436-dfe5-4caf-9560-f14e493f5f88",
            }
        ]
        return (200, {}, flavorprojects)

    def delete_v1_flavorprojects_123(self, **kw):
        return (204, {}, '')

    def post_v1_flavorprojects(self, **kw):
        return (200, {}, generic_flavorproject)

    def get_v1_reservations(self, **kw):
        reservations = [
            {"user_id": "c0645ff94b864d3d84c438d9855f9cea",
             "id": "17664847-0aa0-4a2b-9fe4-073b922914e5",
             "lease_id": None,
             "status": "PENDING_CREATE",
             "end": "2021-04-04T01:00:00",
             "flavor": generic_flavor,
             "project_id": "9427903ca1544f0795ba4117d55ed9b2",
             "start": "2021-04-04T00:00:00",
            },
            {"user_id": "c0645ff94b864d3d84c438d9855f9cea",
             "id": "17664847-0aa0-4a2b-9fe4-073b922914e6",
             "lease_id": "987d558c-3ac3-4bc0-962a-aeb1fbebf5ba",
             "status": "ALLOCATED",
             "end": "2021-04-04T01:00:00",
             "flavor": generic_flavor,
             "project_id": "9427903ca1544f0795ba4117d55ed9b2",
             "start": "2021-04-04T00:00:00",
            }
        ]
        return (200, {}, reservations)

    def get_v1_reservations_123(self, **kw):
        return (200, {}, generic_reservation)

    def post_v1_reservations(self, **kw):
        return (200, {}, generic_reservation)

    def delete_v1_reservations_123(self, **kw):
        return (204, {}, '')

    def get_v1_limits(self, **kw):
        return (200, {}, generic_limits)
