[![documentation](https://img.shields.io/badge/documentation-html-informational)](https://jlecomte.gitlab.io/projects/ansible-roster)
[![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://spdx.org/licenses/MIT.html)
[![pipelines](https://gitlab.com/jlecomte/projects/ansible-roster/badges/master/pipeline.svg)](https://gitlab.com/jlecomte/projects/ansible-roster/pipelines)
[![coverage](https://gitlab.com/jlecomte/projects/ansible-roster/badges/master/coverage.svg)](https://jlecomte.gitlab.io/projects/ansible-roster/coverage/index.html)

# Ansible Roster Inventory Plugin

Roster is an Ansible inventory plugin with focus on groups applied to hosts instead of hosts included in groups. It supports ranges (eg: "[0:9]"), regex hostnames (eg: "(dev|prd)-srv"), file inclusions, and variable merging.

This inventory plugin has been written with [*debops*](https://docs.debops.org/en/master/) in mind.

## Installation from Ansible Galaxy

You can install the latest version from Ansible Galaxy repository.

~~~bash
ansible-galaxy collection install -U julien_lecomte.roster
python3 -mpip install boltons cerberus exrex torxtools
~~~

If you are using *requirement.yml* files for downloading collections and roles, add these lines:

~~~yaml
collections:
  - julien_lecomte.roster
~~~

## Installation from PyPI

You can install the latest version from PyPI package repository.

~~~bash
python3 -mpip install -U ansible-roster
~~~

## Quickstart

Please refer to the [full documentation](https://jlecomte.gitlab.io/projects/ansible-roster/) for all the details.

The roster is a file in yaml format and 'yml' or 'yaml' file extension.

In order for Ansible to use the plugin and parse your roster file, several conditions must be met:

* Your yaml file must contain a line indicating that the file is in the roster format.

* You must activate plugins and enable the roster inventory plugin in your `ansible.cfg`, or in your `.debops.cfg` if using *debops*. If using *debops*, refresh the configuration with *debops project refresh*.

**Sample `ansible.cfg`**

~~~toml
[defaults]
# The following line prevents having to pass -i to ansible-inventory.
# Filename can be anything as long as it has a 'yml' or 'yaml' extension although
inventory = roster.yml

[inventory]
# You must enable the roster plugin if 'auto' does not work for you.
# Use 'roster' if installed via the Python package,
# Use 'julien_lecomte.roster.roster' if installed via Ansible Galaxy
enable_plugins = julien_lecomte.roster.roster
~~~

**Sample `.debops.cfg`**

~~~toml
[ansible inventory]
enabled = roster
# Use 'roster' if installed via the Python package,
# Use 'julien_lecomte.roster.roster' if installed via Ansible Galaxy
enable_plugins = julien_lecomte.roster.roster
~~~

**Sample `roster.yml`**

~~~yaml
---
# This line is mandatory, and enables the plugin differenciating between
# any yaml file and a roster yaml file.
plugin: roster

vars:
  foobar01: "a global var"

groups:
  debian:
    vars:
      distrib: "debian"
  buster:
    parents:
      - debian
    vars:
      release: "buster"
  desktops:
    vars:
      components: "main contrib non-free"

hosts:
  desktop01.internal.example.com:
    groups:
      - desktops
      - buster
~~~

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Locations

  * Documentation: [https://jlecomte.gitlab.io/projects/ansible-roster/](https://jlecomte.gitlab.io/projects/ansible-roster)
  * GitLab: [https://gitlab.com/jlecomte/projects/ansible-roster](https://gitlab.com/jlecomte/projects/ansible-roster)
  * PyPi: [https://pypi.org/project/ansible-roster](https://pypi.org/project/ansible-roster)
  * Galaxy: [https://galaxy.ansible.com/julien_lecomte/roster](https://galaxy.ansible.com/julien_lecomte/roster)

