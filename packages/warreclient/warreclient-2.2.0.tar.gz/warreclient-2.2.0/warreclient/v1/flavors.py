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

from warreclient import base


class Flavor(base.Resource):

    date_fields = ['start', 'end']

    def __repr__(self):
        return "<Flavor %s>" % self.id


class FlavorManager(base.BasicManager):

    base_url = 'v1/flavors'
    resource_class = Flavor

    def update(self, flavor_id, **kwargs):
        return self._update('/%s/%s/' % (self.base_url, flavor_id),
                            data=kwargs)

    def delete(self, flavor_id):
        return self._delete('/%s/%s/' % (self.base_url, flavor_id))

    def free_slots(self, flavor_id, start=None, end=None):
        if start is None:
            start = datetime.date.today()
        elif type(start) == str:
            start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        if end is None:
            end = start + datetime.timedelta(days=30)
        return self._list('/%s/%s/freeslots/?start=%s&end=%s' % (
            self.base_url, flavor_id, start, end), obj_class=None, raw=True)

    def create(self, name, vcpu, memory_mb, disk_gb, description=None,
               active=True, properties=None, max_length_hours=504, slots=1,
               is_public=True, extra_specs={}, start=None, end=None):

        data = {'name': name,
                'description': description,
                'vcpu': int(vcpu),
                'memory_mb': int(memory_mb),
                'disk_gb': int(disk_gb),
                'properties': properties,
                'active': active,
                'max_length_hours': int(max_length_hours),
                'slots': int(slots),
                'is_public': is_public,
                'extra_specs': extra_specs,
                'start': start,
                'end': end}

        return self._create("/%s/" % self.base_url, data=data)
