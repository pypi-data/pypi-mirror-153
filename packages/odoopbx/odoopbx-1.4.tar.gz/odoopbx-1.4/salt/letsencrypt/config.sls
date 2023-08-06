# -*- coding: utf-8 -*-
# vim: ft=sls

{% from "letsencrypt/map.jinja" import letsencrypt with context %}

letsencrypt-config-directory:
  file.directory:
    - name: {{ letsencrypt.config_dir.path }}
    - user: {{ letsencrypt.config_dir.user }}
    - group: {{ letsencrypt.config_dir.group }}
    - dir_mode: {{ letsencrypt.config_dir.mode }}

letsencrypt-config:
  file.managed:
    - name: {{ letsencrypt.config_dir.path }}/cli.ini
    - template: jinja
    - source: salt://letsencrypt/files/cli.ini.jinja
    - user: {{ letsencrypt.config_dir.user }}
    - group: {{ letsencrypt.config_dir.group }}
    - makedirs: true
    - context:
        config: {{ letsencrypt.config | json }}
