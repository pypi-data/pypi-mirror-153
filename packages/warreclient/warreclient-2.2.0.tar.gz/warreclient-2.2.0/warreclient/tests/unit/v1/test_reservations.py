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

import json

from warreclient.v1 import flavors
from warreclient.v1 import reservations

from warreclient.tests.unit import utils
from warreclient.tests.unit.v1 import fakes


class ReservationsTest(utils.TestCase):

    def setUp(self):
        super(ReservationsTest, self).setUp()
        self.cs = fakes.FakeClient()

    def test_reservation_list(self):
        ul = self.cs.reservations.list()
        self.cs.assert_called('GET', '/v1/reservations/')
        for u in ul:
            self.assertIsInstance(u, reservations.Reservation)
        self.assertEqual(2, len(ul))

    def test_reservation_get(self):
        u = self.cs.reservations.get(123)
        self.cs.assert_called('GET', '/v1/reservations/123/')
        self.assertIsInstance(u, reservations.Reservation)
        self.assertEqual('17664847-0aa0-4a2b-9fe4-073b922914e5', u.id)
        self.assertIsInstance(u.flavor, flavors.Flavor)

    def test_create(self):
        data = {'flavor_id': '987d558c-3ac3-4bc0-962a-aeb1fbebf5bb',
                'start': '2021-04-04T00:00:00',
                'end': '2021-04-04T01:00:00',
                'instance_count': 2}

        reservation = self.cs.reservations.create(**data)
        json_data = json.dumps(data)
        self.cs.assert_called('POST', '/v1/reservations/',
                              data=json_data)
        self.assertIsInstance(reservation, reservations.Reservation)

    def test_delete(self):
        self.cs.reservations.delete(123)
        self.cs.assert_called('DELETE', '/v1/reservations/123/')

    def test_reservation_to_dict(self):
        reservation = self.cs.reservations.get(123)
        res_dict = reservation.to_dict()
        self.assertEqual('s2.small', res_dict.get('flavor'))
