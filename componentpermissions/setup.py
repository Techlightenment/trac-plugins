'''
Created on 9 Jun 2011

@author: simon
'''
from setuptools import find_packages, setup

setup(
    name='TracComponentPermissions', version='1.0',
    packages=find_packages(exclude=['*.tests*']),
    entry_points = {
        'trac.plugins': [
            'componentpermissions = componentpermissions.policy',
        ],
    },
)