# -*- coding: utf-8 -*-
# vim: ft=sls
---

{%- set tplroot = tpldir.split('/')[0] %}
{%- from tplroot ~ "/map.jinja" import asterisk with context %}

asterisk-configs:
  file.recurse:
    - name: /etc/asterisk
    - source: salt://asterisk/files/configs
    - template: jinja
    - context: {{ asterisk }}
{%- if not (asterisk.force_update or asterisk.force_config_update) %}
    - replace: False
{%- endif %}
