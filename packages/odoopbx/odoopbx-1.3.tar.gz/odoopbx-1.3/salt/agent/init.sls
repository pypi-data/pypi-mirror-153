include:
  - .config
  - .install
  - .x509
{%- if grains.get('init') in ['systemd',] %}
  - .service
{%- endif %}

