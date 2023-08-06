include:
  - .install
{%- if grains.get('init') in ['systemd',] %}
  - .service
{%- endif %}
