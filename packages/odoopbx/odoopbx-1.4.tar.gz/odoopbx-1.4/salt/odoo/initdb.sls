{%- from "odoo/map.jinja" import odoo with context -%}

odoo-dbuser:
  postgres_user.present:
    - name: {{ odoo.user }}
    - createdb: True
    - encrypted: True
    - db_user: postgres

odoo-init-base:
  cmd.run:
    - name: >
        {{ odoo.src_path }}/odoo-bin -c {{ odoo.conf_path }} -d {{ odoo.db }}
        --no-http --stop-after-init  -i base {{ odoo.initdb_options }}
    - runas: {{ odoo.user }}
    - shell: /bin/bash
    - unless: >
        echo "env['res.users']" |
        {{ odoo.src_path }}/odoo-bin shell --no-http -d {{ odoo.db }}
    - require:
      - odoo-dbuser

odoo-init-asterisk_plus:
  cmd.run:
    - name: >
        {{ odoo.src_path }}/odoo-bin -c {{ odoo.conf_path }} -d {{ odoo.db }}
        --no-http --stop-after-init  -i {{ odoo.addons_init }}
    - runas: {{ odoo.user }}
    - shell: /bin/bash
    - require:
      - odoo-init-base
