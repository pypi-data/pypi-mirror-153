{%- from "letsencrypt/map.jinja" import letsencrypt with context %}

include:
  - ..letsencrypt

letsencrypt-create-webroot-dir:
  file.directory:
    - name: {{ letsencrypt.config['webroot-path'] }}
    - require_in:
      - letsencrypt-config

letsencrypt-activate-cert:
  file.symlink:
    - name: /etc/pki/current
    - target: /etc/letsencrypt/live/fqdn
    - onlyif:
        fun: x509.read_certificate
        certificate: /etc/letsencrypt/live/fqdn/cert.pem
