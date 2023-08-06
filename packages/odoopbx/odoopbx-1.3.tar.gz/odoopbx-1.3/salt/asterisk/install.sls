# -*- coding: utf-8 -*-
# vim: ft=sls
---

{%- set tplroot = tpldir.split('/')[0] %}
{%- from tplroot ~ "/map.jinja" import asterisk with context %}

asterisk-install:
  cmd.run:
    - name: WGET_EXTRA_ARGS="-q" make install
    - cwd: {{ asterisk.src_dir }}
    - creates: /usr/sbin/asterisk
