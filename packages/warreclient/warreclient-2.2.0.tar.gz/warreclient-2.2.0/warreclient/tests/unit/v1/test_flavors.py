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

import datetime
import json

from freezegun import freeze_time

from warreclient.tests.unit import utils
from warreclient.tests.unit.v1 import fakes
from warreclient.v1 import flavors


@freeze_time("2021-05-19")
class FlavorsTest(utils.TestCase):

    def setUp(self):
        super(FlavorsTest, self).setUp()
        self.cs = fakes.FakeClient()

    def test_flavor_list(self):
        ul = self.cs.flavors.list()
        self.cs.assert_called('GET', '/v1/flavors/')
        for u in ul:
            self.assertIsInstance(u, flavors.Flavor)
        self.assertEqual(2, len(ul))

    def test_flavor_get(self):
        u = self.cs.flavors.get(123)
        self.cs.assert_called('GET', '/v1/flavors/123/')
        self.assertIsInstance(u, flavors.Flavor)
        self.assertEqual('d6506b62-13c2-4dec-a556-b306bb5e959f', u.id)

    def test_update(self):
        flavor = self.cs.flavors.update(123, slots=2)
        self.cs.assert_called('PATCH', '/v1/flavors/123/',
                              json.dumps({'slots': 2}))
        self.assertIsInstance(flavor, flavors.Flavor)
        self.assertEqual(2, flavor.slots)

    def test_create(self):
        data = {'name': 'foo',
                'vcpu': 20,
                'memory_mb': 30,
                'disk_gb': 40,
                'description': 'foobar',
                'active': False,
                'properties': 'foo=bar',
                'max_length_hours': 24,
                'slots': 7,
                'is_public': False,
                'extra_specs': {'foo': 'bar', 'bar': 'foo'},
                'start': '2021-04-04T00:00:00',
                'end': '2021-04-04T01:00:00'}

        flavor = self.cs.flavors.create(**data)
        json_data = json.dumps(data)
        self.cs.assert_called('POST', '/v1/flavors/',
                              data=json_data)
        self.assertIsInstance(flavor, flavors.Flavor)

    def test_create_defaults(self):
        defaults = {
            'description': None,
            'active': True,
            'properties': None,
            'max_length_hours': 504,
            'slots': 1,
            'is_public': True,
            'extra_specs': {},
            'start': None,
            'end': None}

        data = {'name': 'foo',
                'vcpu': 20,
                'memory_mb': 30,
                'disk_gb': 40}
        flavor = self.cs.flavors.create(**data)
        data.update(defaults)
        json_data = json.dumps(data)
        self.cs.assert_called('POST', '/v1/flavors/',
                              data=json_data)
        self.assertIsInstance(flavor, flavors.Flavor)

    def test_delete(self):
        self.cs.flavors.delete(123)
        self.cs.assert_called('DELETE', '/v1/flavors/123/')

    def test_free_slots(self):
        free_slots = self.cs.flavors.free_slots(123)
        self.cs.assert_called(
            'GET',
            '/v1/flavors/123/freeslots/?start=2021-05-19&end=2021-06-18')
        self.assertIsInstance(free_slots, list)
        self.assertIsInstance(free_slots[0], dict)

    def test_free_slots_end(self):
        self.cs.flavors.free_slots(123, end='2021-09-01')
        self.cs.assert_called(
            'GET',
            '/v1/flavors/123/freeslots/?start=2021-05-19&end=2021-09-01')

    def test_free_slots_end_date(self):
        self.cs.flavors.free_slots(123, end=datetime.date(2021, 8, 31))
        self.cs.assert_called(
            'GET',
            '/v1/flavors/123/freeslots/?start=2021-05-19&end=2021-08-31')

    def test_free_slots_start(self):
        self.cs.flavors.free_slots(123, start='2021-07-01')
        self.cs.assert_called(
            'GET',
            '/v1/flavors/123/freeslots/?start=2021-07-01&end=2021-07-31')

    def test_free_slots_start_date(self):
        self.cs.flavors.free_slots(123, start=datetime.date(2021, 7, 1))
        self.cs.assert_called(
            'GET',
            '/v1/flavors/123/freeslots/?start=2021-07-01&end=2021-07-31')
