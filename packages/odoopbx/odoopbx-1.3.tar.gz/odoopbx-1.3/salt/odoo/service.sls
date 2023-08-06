{%- from "odoo/map.jinja" import odoo with context -%}

odoo-service:
  file.managed:
    - name: /etc/systemd/system/odoo.service
    - source: salt://odoo/templates/odoo.service
    - template: jinja
    - context: {{ odoo }}
    - replace: {{ odoo.force_config_update }}
  service.enabled:
    - name: odoo
    - enable: true
