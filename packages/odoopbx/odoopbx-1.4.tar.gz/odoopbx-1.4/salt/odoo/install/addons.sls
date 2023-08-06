{%- from "odoo/map.jinja" import odoo with context -%}

addons-cloned-{{ odoo.version }}:
  git.latest:
    - name: https://github.com/odoopbx/addons.git
    - branch: {{ odoo.version }}
    - depth: 1
    - fetch_tags: False
    - rev: {{ odoo.version }}
    - target: {{ odoo.addons_path }}
    {%- if odoo.force_update %}
    - force_clone: True
    - foce_checkout: True
    - force_reset: true
    {%- else %}
    - creates: {{ odoo.addons_path }}/.git
    {%- endif %}

addons-pip-reqs:
  pip.installed:
    - upgrade: {{ odoo.force_update }}
    - requirements: {{ odoo.addons_path }}/requirements.txt
    - require:
      - addons-cloned-{{ odoo.version }}
    - retry:
        attempts: 2
