{% if grains.os_family == "Debian" %}
include:
  - agent
  - asterisk
  - postgres
  - odoo
  - odoo.initdb
  - nginx
{% else %}
not-yet-supported:
  test.show_notification:
    - text: Sorry, {{ grains.os_family }} is not supported yet
{% endif %}

{%- if "virtual_subtype" not in grains %}
odoopbx-configure:
  host.present:
    - ip: 127.0.0.1
    - names:
        - agent
        - odoo
        - asterisk
{%- endif %}

{%- if grains.get('init') in ['systemd',] %}
odoopbx-run-services:
  service.running:
    - names:
      - odoo
      - salt-master
      - salt-api
      - salt-minion
{%- endif %}
