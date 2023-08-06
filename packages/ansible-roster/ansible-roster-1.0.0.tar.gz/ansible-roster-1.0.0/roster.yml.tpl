# vim: ft=yaml
---
# This is a sample, commented, roster file in order to generate an ansible
# inventory.
#
# If not using debops, then your ansible.cfg must enable plugin:
#
#   [defaults]
#   inventory = roster.yml
#
#   [inventory]
#   # Use 'roster' if installed via the Python package,
#   # Use 'julien_lecomte.roster.roster' if installed via Ansible Galaxy
#   enable_plugins = julien_lecomte.roster.roster
#
# If using debops, then your .debops.cfg must enable the plugin:
#
#   [ansible inventory]
#   enabled = roster
#   # Use 'roster' if installed via the Python package,
#   # Use 'julien_lecomte.roster.roster' if installed via Ansible Galaxy
#   enable_plugins = julien_lecomte.roster.roster
#
---
# This line is mandatory, and enables the plugin differenciating between
# any yaml file and a roster yaml file.
plugin: roster

# Variables are handled with priority:
#   0 - values from vars: (lowest priority)
#   1 - values from groups.*.vars
#   2 - values from hosts.*.vars
# With 0 being the lowest priority
#

vars:
  var__foobar01: true
  components: "main contrib"

groups:
  debian:
    vars:
      distrib: "debian"

  stretch:
    parents:
      - debian
    vars:
      release: "stretch"

  buster:
    parents:
      - debian
    vars:
      release: "buster"

  desktops:
    vars:
      components: "main contrib non-free"

  server:
    vars:
      components: "main"

hosts:
  desktop01.internal.example.com:
    groups:
      - desktops
      - buster
    vars:
      var__foobar01: false

  server01.internal.example.com:
    groups:
      - servers
      - debian

  server01.example.com:
    groups:
      - servers
      - debian

  # items that start with a dot will be ignored
  .server02.example.com:
    groups:
      - servers
      - debian

