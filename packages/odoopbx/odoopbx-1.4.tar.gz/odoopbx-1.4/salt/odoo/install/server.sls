{%- from "odoo/map.jinja" import odoo with context -%}

odoo-pkg-reqs:
  pkg.installed:
    - pkgs:
      - git
      - libxml2-dev
      - libxslt1-dev
      - libjpeg-dev
      - libldap2-dev
      - libsasl2-dev
      - libpq-dev
      - python3-dev
      - sudo

odoo-pip-upgraded:
  cmd.run:
    - name: pip3 install --upgrade pip
    - reload_modules: true
    - onfail:
      - odoo-pip-reqs
      - addons-pip-reqs

odoo-user:
  user.present:
    - name: {{ odoo.user }}
    - usergroup: True
    - shell: /bin/bash

odoo-make-dirs:
  file.directory:
    - names:
      - {{ odoo.data_path }}/filestore:
        - user: {{ odoo.user }}
        - dir_mode: 750
      - {{ odoo.addons_path }}:
        - group: {{ odoo.user }}
    - makedirs: True

odoo-cloned-{{ odoo.version }}:
  git.latest:
    - name: https://github.com/odoo/odoo.git
    - branch: {{ odoo.version }}
    - depth: 1
    - fetch_tags: False
    - rev: {{ odoo.version }}
    - target: {{ odoo.src_path }}
    - require:
      - odoo-pkg-reqs
    {%- if odoo.force_update %}
    - force_clone: True
    - foce_checkout: True
    - force_reset: True
    {%- else %}
    - creates: {{ odoo.src_path }}/.git
    {%- endif %}

odoo-pip-reqs:
  pip.installed:
    - upgrade: {{ odoo.force_update }}
    - requirements: {{ odoo.src_path }}/requirements.txt
    - require:
      - odoo-cloned-{{ odoo.version }}
    - retry:
        attempts: 2

odoo-configs:
  file.managed:
    - name: {{ odoo.conf_path }}
    - source: salt://odoo/templates/odoo.conf
    - group: {{ odoo.user }}
    - mode: 640
    - makedirs: True
    - template: jinja
    - context: {{ odoo }}
    - replace: {{ odoo.force_config_update }}

odoo-environment:
  file.keyvalue:
    - name: /etc/environment
    - key: ODOO_RC
    - value: {{ odoo.conf_path }}
    - append_if_not_found: True
