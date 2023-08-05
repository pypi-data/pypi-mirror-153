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


class Limits(base.Resource):
    """A collection of AbsoluteLimit objects."""

    def __repr__(self):
        return "<Limits>"

    @property
    def absolute(self):
        for (name, value) in self._info['absolute'].items():
            yield AbsoluteLimit(name, value)


class AbsoluteLimit(object):
    """Data model that represents a single absolute limit."""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return self.value == other.value and self.name == other.name

    def __repr__(self):
        return "<AbsoluteLimit: name=%s>" % (self.name)


class LimitsManager(base.Manager):
    """Manager object used to interact with limits resource."""

    resource_class = Limits

    def get(self, project_id=None):
        """Get a specific extension.

        :rtype: :class:`Limits`
        """
        opts = {}
        if project_id:
            opts['project_id'] = project_id
        return self._get("/v1/limits", params=opts)
