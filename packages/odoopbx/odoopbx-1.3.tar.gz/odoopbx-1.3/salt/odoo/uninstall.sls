{%- from "odoo/map.jinja" import odoo with context -%}

{%- if grains.get('init') in ['systemd',] %}
odoo-stop:
  service.dead:
    - name: odoo
    - enable: False
  file.absent:
    - name: /etc/systemd/system/odoo.service
{%- endif %}

odoo-remove:
  file.absent:
    - names:
      - {{ odoo.src_path }}
      - {{ odoo.data_path }}
      - {{ odoo.addons_path }}
      - {{ odoo.conf_path }}
