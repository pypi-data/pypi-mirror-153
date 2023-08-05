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

from warreclient import base
from warreclient.v1 import flavors


class Reservation(base.Resource):

    date_fields = ['start', 'end']

    def __init__(self, manager, info, loaded=False, resp=None):
        super(Reservation, self).__init__(manager, info, loaded, resp)
        self.flavor = flavors.Flavor(None, self.flavor, loaded=True)

    def __repr__(self):
        return "<Reservation %s>" % self.id

    def to_dict(self):
        res = super(Reservation, self).to_dict()
        res['flavor'] = res.get('flavor', {}).get('name')
        return res


class ReservationManager(base.BasicManager):

    base_url = 'v1/reservations'
    resource_class = Reservation

    def delete(self, reservation_id):
        return self._delete('/%s/%s/' % (self.base_url, reservation_id))

    def create(self, flavor_id, start, end, instance_count=1):
        data = {'flavor_id': flavor_id,
                'start': start,
                'end': end,
                'instance_count': instance_count}
        return self._create("/%s/" % self.base_url, data=data)
