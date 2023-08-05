#!/usr/bin/env python

import setuptools

from pbr.packaging import parse_requirements

entry_points = {
    'openstack.cli.extension':
    ['warre = warreclient.osc.plugin'],
    'openstack.warre.v1':
    [
        'warre reservation list = warreclient.osc.v1.reservations:ListReservations',
        'warre reservation show = warreclient.osc.v1.reservations:ShowReservation',
        'warre reservation create = warreclient.osc.v1.reservations:CreateReservation',
        'warre reservation delete = warreclient.osc.v1.reservations:DeleteReservation',
        'warre flavor list = warreclient.osc.v1.flavors:ListFlavors',
        'warre flavor show = warreclient.osc.v1.flavors:ShowFlavor',
        'warre flavor create = warreclient.osc.v1.flavors:CreateFlavor',
        'warre flavor delete = warreclient.osc.v1.flavors:DeleteFlavor',
        'warre flavor set = warreclient.osc.v1.flavors:UpdateFlavor',
        'warre flavor access grant = warreclient.osc.v1.flavors:GrantAccess',
        'warre flavor access revoke = warreclient.osc.v1.flavors:RevokeAccess',
        'warre flavor access list = warreclient.osc.v1.flavors:ListAccess',
        'warre flavor free-slots = warreclient.osc.v1.flavors:FlavorSlots',
        'warre limits = warreclient.osc.v1.limits:ListLimits',
    ]
}


setuptools.setup(
    name='warreclient',
    version='2.2.0',
    description=('Client for the Warre system'),
    author='Sam Morrison',
    author_email='sorrison@gmail.com',
    url='https://github.com/NeCTAR-RC/python-warreclient',
    packages=[
        'warreclient',
    ],
    include_package_data=True,
    setup_requires=['pbr>=3.0.0'],
    install_requires=parse_requirements(),
    license="Apache",
    zip_safe=False,
    classifiers=(
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ),
    entry_points=entry_points,
)
