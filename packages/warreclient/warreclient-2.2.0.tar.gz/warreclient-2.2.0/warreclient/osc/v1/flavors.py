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
import logging

from osc_lib.command import command
from osc_lib import utils as osc_utils

from warreclient import exceptions


class ListFlavors(command.Lister):
    """List flavors."""

    log = logging.getLogger(__name__ + '.ListFlavors')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre
        kwargs = {}
        if parsed_args.all:
            kwargs['all_projects'] = True
        if parsed_args.category:
            kwargs['category'] = parsed_args.category
        if parsed_args.availability_zone:
            kwargs['availability_zone'] = parsed_args.availability_zone
        flavors = client.flavors.list(**kwargs)
        columns = ['id', 'name', 'memory_mb', 'disk_gb', 'vcpu',
                   'active', 'is_public']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in flavors)
        )

    def get_parser(self, prog_name):
        parser = super(ListFlavors, self).get_parser(prog_name)
        parser.add_argument(
            '--all',
            action='store_true',
            default=False,
            help="List all flavors"
        )
        parser.add_argument(
            '--category',
            help="Filter by category field"
        )
        parser.add_argument(
            '--availability-zone',
            help="Filter by availability_zone field"
        )
        return parser


class FlavorCommand(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(FlavorCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('ID of flavor')
        )
        return parser

    def _get_flavor(self, id):
        client = self.app.client_manager.warre
        try:
            flavor = client.flavors.get(id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
        return flavor


class ShowFlavor(FlavorCommand):
    """Show flavor details."""

    log = logging.getLogger(__name__ + '.ShowFlavor')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        flavor = self._get_flavor(parsed_args.id)
        return self.dict2columns(flavor.to_dict())


class CreateFlavor(command.ShowOne):
    """Create an flavor."""

    log = logging.getLogger(__name__ + '.CreateFlavor')

    def get_parser(self, prog_name):
        parser = super(CreateFlavor, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Name of the flavor'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Description of the flavor'
        )
        parser.add_argument(
            '--vcpu',
            metavar='<vcpu>',
            required=True,
            type=int,
            help="Number of VCPUs"
        )
        parser.add_argument(
            '--memory',
            metavar='<memory>',
            required=True,
            type=int,
            help="Amount of memory in MB"
        )
        parser.add_argument(
            '--disk',
            metavar='<disk>',
            required=True,
            type=int,
            help="Amount of disk in GB"
        )
        parser.add_argument(
            '--properties',
            metavar='<properties>',
            help="Properties for flavor"
        )
        parser.add_argument(
            '--max-length-hours',
            metavar='<max_length_hours>',
            required=True,
            type=int,
            help="Maximum reservation time in hours"
        )
        parser.add_argument(
            '--slots',
            metavar='<slots>',
            required=True,
            type=int,
            help="Amount of slots available for this flavor"
        )
        parser.add_argument(
            '--disable',
            action='store_true',
            default=False,
            help="Flavor is disabled (default: false)"
        )
        parser.add_argument(
            '--private',
            action='store_true',
            default=False,
            help="Flavor is private (default: false)"
        )
        parser.add_argument(
            '--extra-specs',
            metavar='<extra_specs>',
            default={},
            help='A dictionary of extra Specs for the flavor'
        )
        parser.add_argument(
            '--start',
            metavar='<start>',
            default=None,
            help='Start time (YYYY-MM-DD HH:MM) UTC TZ of flavor. Used to '
                 'restrict when a flavor can be used',
        )
        parser.add_argument(
            '--end',
            metavar='<end>',
            default=None,
            help='End time (YYYY-MM-DD HH:MM) UTC TZ of flavor. Used to '
                'restrict when a flavor can be used',
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.warre

        is_public = not parsed_args.private
        active = not parsed_args.disable

        try:
            extra_specs = json.loads(parsed_args.extra_specs) \
                if parsed_args.extra_specs else parsed_args.extra_specs

        except json.JSONDecodeError:
            raise exceptions.CommandError("Extra specs not valid json")

        fields = {'name': parsed_args.name,
                  'vcpu': parsed_args.vcpu,
                  'memory_mb': parsed_args.memory,
                  'disk_gb': parsed_args.disk,
                  'description': parsed_args.description,
                  'active': active,
                  'properties': parsed_args.properties,
                  'max_length_hours': parsed_args.max_length_hours,
                  'slots': parsed_args.slots,
                  'is_public': is_public,
                  'extra_specs': extra_specs,
                  'start': parsed_args.start,
                  'end': parsed_args.end}

        flavor = client.flavors.create(**fields)
        flavor_dict = flavor.to_dict()
        return self.dict2columns(flavor_dict)


class UpdateFlavor(FlavorCommand):
    """Update a flavor."""

    log = logging.getLogger(__name__ + '.UpdateFlavor')

    def get_parser(self, prog_name):
        parser = super(UpdateFlavor, self).get_parser(prog_name)
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Description of the flavor'
        )
        parser.add_argument(
            '--max-length-hours',
            metavar='<max_length_hours>',
            type=int,
            help="Maximum reservation time in hours"
        )
        parser.add_argument(
            '--slots',
            metavar='<slots>',
            type=int,
            help="Amount of slots available for this flavor"
        )
        parser.add_argument(
            '--active',
            action='store_true',
            help="Enable Flavor"
        )
        parser.add_argument(
            '--disable',
            action='store_true',
            help="Disable Flavor"
        )
        parser.add_argument(
            '--public',
            action='store_true',
            help="Flavor is public"
        )
        parser.add_argument(
            '--private',
            action='store_true',
            help="Flavor is private"
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre

        if parsed_args.private and parsed_args.public:
            raise exceptions.CommandError(
                "Can't specify --private and --public")
        if parsed_args.active and parsed_args.disable:
            raise exceptions.CommandError(
                "Can't specify --active and --disable")

        flavor = self._get_flavor(parsed_args.id)
        data = {}
        if parsed_args.description:
            data['description'] = parsed_args.description
        if parsed_args.max_length_hours:
            data['max_length_hours'] = parsed_args.max_length_hours
        if parsed_args.slots:
            data['slots'] = parsed_args.slots
        if parsed_args.public:
            data['is_public'] = True
        if parsed_args.private:
            data['is_public'] = False
        if parsed_args.active:
            data['active'] = True
        if parsed_args.disable:
            data['active'] = False
        flavor = client.flavors.update(flavor_id=parsed_args.id, **data)
        flavor_dict = flavor.to_dict()
        return self.dict2columns(flavor_dict)


class DeleteFlavor(FlavorCommand):
    """Delete flavor."""

    log = logging.getLogger(__name__ + '.DeleteFlavor')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre

        try:
            client.flavors.delete(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return [], []


class GrantAccess(command.ShowOne):
    """Grant access to a flavor."""

    log = logging.getLogger(__name__ + '.GrantAccess')

    def get_parser(self, prog_name):
        parser = super(GrantAccess, self).get_parser(prog_name)
        parser.add_argument(
            'flavor_id',
            metavar='<flavor_id>',
            help='Flavor ID'
        )
        parser.add_argument(
            'project_id',
            metavar='<project_id>',
            help='Project ID'
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.warre

        fields = {'flavor_id': parsed_args.flavor_id,
                  'project_id': parsed_args.project_id}

        flavorproject = client.flavorprojects.create(**fields)
        fp_dict = flavorproject.to_dict()
        return self.dict2columns(fp_dict)


class RevokeAccess(command.ShowOne):
    """Revokes access to a flavor."""

    log = logging.getLogger(__name__ + '.RevokeAccess')

    def get_parser(self, prog_name):
        parser = super(RevokeAccess, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help='Access ID'
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre
        try:
            client.flavorprojects.delete(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return [], []


class ListAccess(command.Lister):
    """List flavors."""

    log = logging.getLogger(__name__ + '.ListAccess')

    def get_parser(self, prog_name):
        parser = super(ListAccess, self).get_parser(prog_name)
        parser.add_argument(
            '--flavor-id',
            default=None,
            metavar='<flavor_id>',
            help='Filter by Flavor ID'
        )
        parser.add_argument(
            '--project-id',
            default=None,
            metavar='<project_id>',
            help='Filter by Project ID'
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre

        flavorprojects = client.flavorprojects.list(
            flavor_id=parsed_args.flavor_id, project_id=parsed_args.project_id)
        columns = ['id', 'flavor', 'project_id']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in flavorprojects)
        )


class FlavorSlots(command.Lister):
    """Show flavor free slots."""

    log = logging.getLogger(__name__ + '.FlavorSlots')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre
        slots = client.flavors.free_slots(parsed_args.id, parsed_args.start,
            parsed_args.end)
        columns = ['start', 'end']
        return (
            columns,
            (osc_utils.get_dict_properties(q, columns) for q in slots)
        )

    def get_parser(self, prog_name):
        parser = super(command.Lister, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('ID of flavor')
        )
        parser.add_argument(
            '--start',
            metavar='<start>',
            default=None,
            help='Date (YYYY-MM-DD)',
        )
        parser.add_argument(
            '--end',
            metavar='<end>',
            default=None,
            help='Date (YYYY-MM-DD)',
        )
        return parser
