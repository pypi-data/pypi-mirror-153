#
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


from warreclient.tests.unit import utils
from warreclient.tests.unit.v1 import fakes
from warreclient.v1 import limits


class LimitsTest(utils.TestCase):

    def setUp(self):
        super(LimitsTest, self).setUp()
        self.cs = fakes.FakeClient()

    def test_get_limits(self):
        obj = self.cs.limits.get()
        self.cs.assert_called('GET', '/v1/limits')
        self.assertIsInstance(obj, limits.Limits)

    def test_rate_absolute_limits(self):
        obj = self.cs.limits.get()

        expected = [
            limits.AbsoluteLimit("maxHours", 49),
            limits.AbsoluteLimit("maxReservations", 10),
            limits.AbsoluteLimit("totalHoursUsed", 27),
            limits.AbsoluteLimit("totalReservationsUsed", 4)
        ]
        abs_limits = list(obj.absolute)
        self.assertEqual(len(abs_limits), len(expected))

        for limit in abs_limits:
            self.assertIn(limit, expected)
