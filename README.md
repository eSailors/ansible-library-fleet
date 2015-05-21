Ansible Fleet library
==========

# Table of Contents
- [Description](#description)
- [Requirements](#requirements)
- [Examples](#examples)
- [License](#license)
- [Author information](#author information)

# Description

Ansible library to manage Fleet units. This module uses a local installed __fleetctl__ binary and not the
rest interface!

If __fleetctl__ is not inside PATH use Ansible's environment declaration.

# Requirements

- Ansible must be installed
- [fleetctl] must be installed on the system where Ansible is running on.

# Example

Ensure a unit file is submitted
```yaml
- name: Ensure unit file is submitted
  fleet_unit:
    name: /tmp/fleet_unit.service
    state: submitted
```

Ensure a service provided by a unit file is running

```yaml
- name: Ensure service is running
  fleet_unit: /tmp/fleet_unit.service
  state: running
```

Ensure all services defined by unit files in a directory are loaded together
```yaml
- name: Ensure services are loaded
  fleet_unit:
    path: /tmp/mydirectory
    state: loaded
```
# License

Copyright 2015 Thomas Krahn

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# Author information

[Thomas Krahn]

[Thomas Krahn]: mailto:ntbc@gmx.net
[fleetctl]: https://github.com/coreos/fleet/tree/master/fleetctl
