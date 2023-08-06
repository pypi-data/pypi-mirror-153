# -*- coding: utf-8 -*-
# vim: ft=sls

{% from "letsencrypt/map.jinja" import letsencrypt with context %}

{% if letsencrypt.install_method == 'package' %}
letsencrypt-service-timer:
  service.running:
    - name: {{ letsencrypt.service }}
    - enable: true
    - watch:
      - pkg: letsencrypt-client
{% endif %}
