ansible-library-fleet
-------------------

# Description
Ansible library to manage Fleet units. The module uses a local installed __fleetctl__ binary and not the rest interface!

# Requirements
- Ansible must be installed
- [fleetctl] must be installed on the system where Ansible is running on.

# Example
Ensure a unit file is submitted
```
- name: Ensure submitted unit file
  fleet_unit:
    name: /tmp/fleet_unit.service
    state: submitted
```

Ensure a service provided by a unit file is running
```
- name: Ensure service is running
  fleet_unit: /tmp/fleet_unit.service
  state: running
```

Ensure all services defined by unit files in a directory are loaded together
```
- name: Ensure services are loaded
  fleet_unit:
    path: /tmp/mydirectory
    state: loaded
```

# Author information
[Thomas Krahn]

[Thomas Krahn]: mailto:ntbc@gmx.net
[fleetctl]: https://github.com/coreos/fleet/tree/master/fleetctl
