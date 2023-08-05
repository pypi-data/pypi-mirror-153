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

from warreclient.v1 import flavorprojects

from warreclient.tests.unit import utils
from warreclient.tests.unit.v1 import fakes


class FlavorProjectsTest(utils.TestCase):

    def setUp(self):
        super(FlavorProjectsTest, self).setUp()
        self.cs = fakes.FakeClient()

    def test_flavorproject_list(self):
        ul = self.cs.flavorprojects.list()
        self.cs.assert_called('GET', '/v1/flavorprojects/')
        for u in ul:
            self.assertIsInstance(u, flavorprojects.FlavorProject)
        self.assertEqual(2, len(ul))

    def test_delete(self):
        self.cs.flavorprojects.delete(123)
        self.cs.assert_called('DELETE', '/v1/flavorprojects/123/')

    def test_create(self):
        data = {'project_id': 'xyz', 'flavor_id': 'abc'}

        flavor = self.cs.flavorprojects.create(**data)
        json_data = json.dumps(data)
        self.cs.assert_called('POST', '/v1/flavorprojects/', data=json_data)
        self.assertIsInstance(flavor, flavorprojects.FlavorProject)
