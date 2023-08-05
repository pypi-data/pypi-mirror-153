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


class FlavorProject(base.Resource):
    def __repr__(self):
        return "<FlavorProject %s>" % self.attributes.get('id')


class FlavorProjectManager(base.Manager):

    base_url = 'v1/flavorprojects'
    resource_class = FlavorProject

    def delete(self, flavor_id):
        return self._delete('/%s/%s/' % (self.base_url, flavor_id))

    def create(self, flavor_id, project_id):
        data = {"flavor_id": flavor_id, "project_id": project_id}
        return self._create("/%s/" % self.base_url, data=data)

    def list(self, flavor_id=None, project_id=None):
        kwargs = {}
        if flavor_id is not None:
            kwargs['flavor_id'] = flavor_id
        if project_id is not None:
            kwargs['project_id'] = project_id
        return self._list('/%s/' % self.base_url, params=kwargs)
