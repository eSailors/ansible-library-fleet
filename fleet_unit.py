#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

FLEETCTL_BIN = 'fleetctl'

FLEET_MATRIX = [{'ensure_state': 'submitted', 'unit_state': 'inactive', 'command': 'submit'},
                {'ensure_state': 'loaded', 'unit_state': 'loaded', 'command': 'load'},
                {'ensure_state': 'started', 'unit_state': 'launched', 'command': 'start'},
                {'ensure_state': 'stopped', 'unit_state': 'loaded', 'command': 'stop'},
                {'ensure_state': 'unloaded', 'unit_state': 'inactive', 'command': 'unload'}]


def fleetctl(command, command_options='', global_options='', arguments=''):
    cmd = '{fleetctl} {global_options} {command} {command_options} {arguments}'.format(fleetctl=FLEETCTL_BIN,
                                                                                       global_options=global_options,
                                                                                       command=command,
                                                                                       command_options=command_options,
                                                                                       arguments=arguments)
    rc, out, err = module.run_command(cmd)
    if rc != 0:
        module.fail_json(msg='Error while executing "{cmd}": {error}'.format(cmd=cmd, error=err))
    return out


def get_fleet_units():
    driver = module.params['driver']
    out = fleetctl(command='list-unit-files', arguments='--no-legend', global_options='--driver="{driver}"'.format(driver=driver))
    return [re.sub(r'(\t+?)\1', r'\1', line).split('\t') for line in out.split('\n') if line]


def is_unit_submitted(unit, unit_files):
    # Determine if unit is an instance unit (http://0pointer.de/blog/projects/instances.html)
    # True: apache@8080.service, False: apache@.service, myapp.service
    if re.search(r'@.+\.', unit):
        unit_file_name = re.sub(r'(.+@)(.+)(\..+)', r'\1\3', unit)
    else:
        unit_file_name = unit

    for line in unit_files:
        if line[0] == unit_file_name:
            return True
    return False


def get_unit_name(unit):
    return unit[0]


def get_unit_state(unit):
    if unit:
        return unit[3]
    return None


def get_unit(name, units):
    result = None
    if units:
        for unit in units:
            if get_unit_name(unit) == name:
                result = unit
                break
    return result


def unit_has_desired_state(unit, state):
    fleet_state = [item for item in FLEET_MATRIX if item.get('ensure_state') == state]
    return fleet_state[0].get('unit_state') == get_unit_state(unit)


def get_state_command(state):
    return ' '.join([item.get('command') for item in FLEET_MATRIX if item.get('ensure_state') == state])


def ensure():
    name = module.params['name']
    path = module.params['path']
    driver = module.params['driver']
    state = module.params['state']

    if path:
        try:
            unit_files = [os.path.join(path, filename) for filename in os.listdir(path)]
        except OSError as e:
            module.fail_json(msg='Could not list files in {path}: {error}'.format(path=path, error=e.strerror))
    else:
        unit_files = [os.path.join(os.path.dirname(name), os.path.basename(name))]

    fleet_units = get_fleet_units()
    unit_files_to_handle = list()
    for item in unit_files:
        unit = get_unit(os.path.basename(item), fleet_units)
        if state == 'submitted' and unit:
            continue
        if state == 'destroyed' and not unit:
            continue
        if not unit_has_desired_state(unit, state):
            unit_files_to_handle.append(item)

    if len(unit_files_to_handle) > 0:
        fleet_command = get_state_command(state)
        fleet_command_options = ' '.join([item for item in unit_files_to_handle])
        # module.fail_json(msg='Command: {cmd}\nOptions: {opts}'.format(cmd=fleet_command, opts=fleet_command_options))
        fleetctl(command=fleet_command,
                 command_options=fleet_command_options,
                 global_options='--driver="{driver}"'.format(driver=driver))
        return True, unit_files_to_handle

    return False, unit_files_to_handle


def main():
    global module
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', default=None),
            path=dict(type='str', default=None),
            driver=dict(type='str', default='etcd',
                       choices=['etcd', 'api']),
            state=dict(type='str', default='started',
                       choices=['submitted', 'loaded', 'started', 'stopped', 'unloaded', 'destroyed']),
        ),
        required_one_of=[('name', 'path')],
        supports_check_mode=True
    )

    changed, units = ensure()
    module.exit_json(changed=changed, units=units)

# import module snippets
from ansible.module_utils.basic import *

main()
