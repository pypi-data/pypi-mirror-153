# -*- coding: utf-8 -*-
# vim: ft=sls
---

{%- set tplroot = tpldir.split('/')[0] %}
{%- from tplroot ~ "/map.jinja" import asterisk with context %}

asterisk-uninstall:
  file.absent:
    - names:
        - {{ asterisk.src_dir }}
        - /etc/asterisk
        - /etc/logrotate.d/asterisk
        - /usr/include/asterisk
        - /usr/lib/asterisk
        - /usr/sbin/asterisk
        - /var/lib/asterisk
        - /var/log/asterisk
        - /var/run/asterisk
        - /var/spool/asterisk
