# -*- coding: utf-8 -*-
# vim: ft=sls

{% from "letsencrypt/map.jinja" import letsencrypt with context %}

{% if letsencrypt.install_method == 'package' %}
  {% set check_cert_cmd = letsencrypt._cli_path ~ ' certificates --cert-name' %}
  {% set renew_cert_cmd = letsencrypt._cli_path ~ ' renew' %}
  {% set create_cert_cmd = letsencrypt._cli_path %}

  {% set old_check_cert_cmd_state = 'absent' %}
  {% set old_renew_cert_cmd_state = 'absent' %}
  {% set old_cron_state = 'absent' %}

{% else %}
  {% set check_cert_cmd = '/usr/local/bin/check_letsencrypt_cert.sh' %}
  {% set renew_cert_cmd = '/usr/local/bin/renew_letsencrypt_cert.sh' %}
  {% if letsencrypt.install_method == 'pip' %}
    {% set create_cert_cmd = letsencrypt.cli_install_dir ~ '/bin/certbot' %}
  {% else %}
    {% set create_cert_cmd = letsencrypt.cli_install_dir ~ '/letsencrypt-auto' %}
  {% endif %}

  {% set old_check_cert_cmd_state = 'managed' %}
  {% set old_renew_cert_cmd_state = 'managed' %}
  {% set old_cron_state = 'present' %}

{{ check_cert_cmd }}:
  file.{{ old_check_cert_cmd_state }}:
    - template: jinja
    - source: salt://letsencrypt/files/check_letsencrypt_cert.sh.jinja
    - mode: 755

{{ renew_cert_cmd }}:
  file.{{ old_renew_cert_cmd_state }}:
    - template: jinja
    - source: salt://letsencrypt/files/renew_letsencrypt_cert.sh.jinja
    - mode: 755
    - require:
      - file: {{ check_cert_cmd }}

{% endif %}

{%- set default_authenticator = '--authenticator ' ~ letsencrypt.authenticators['default']
                                if letsencrypt.authenticators['default'] is defined else '' %}

{%- set default_installer = '--installer ' ~ letsencrypt.installers['default']
                            if letsencrypt.installers['default'] is defined else '' %}

{% for setname, domainlist in letsencrypt.domainsets.items() %}

  # Set an authenticator and a installer for the domainset or use defaults set above
  {%- set authenticator = '--authenticator ' ~ letsencrypt.authenticators[setname]
                          if letsencrypt.authenticators[setname] is defined else default_authenticator %}
  {%- set installer = '--installer ' ~ letsencrypt.installers[setname]
                      if letsencrypt.installers[setname] is defined else default_installer %}

# domainlist[0] represents the "CommonName", and the rest
# represent SubjectAlternativeNames
create-initial-cert-{{ setname }}-{{ domainlist | join('+') }}:
  cmd.run:
    - name: |
        {{ create_cert_cmd }} {{ letsencrypt.create_init_cert_subcmd }} \
          --quiet \
          --non-interactive \
          {{ authenticator }} \
          {{ installer }} \
          --cert-name {{ setname }} \
          -d {{ domainlist|join(' -d ') }}
      {% if letsencrypt.install_method != 'package' %}
    - cwd: {{ letsencrypt.cli_install_dir }}
      {% endif %}
    - unless:
      {% if letsencrypt.install_method == 'package' %}
      - fun: cmd.run
        python_shell: true
        cmd: |
          {{ check_cert_cmd }} {{ setname }} \
            -d {{ domainlist|join(' -d ') }} | \
            /bin/grep -q "Certificate Name: {{ setname }}"
      {% else %}
      - {{ check_cert_cmd }} {{ setname }} {{ domainlist | join(' ') }}
      {% endif %}
    - require:
      {% if letsencrypt.install_method == 'package' %}
      - pkg: letsencrypt-client
      {% else %}
      - file: {{ check_cert_cmd }}
      {% endif %}
      - file: letsencrypt-config

letsencrypt-crontab-{{ setname }}-{{ domainlist[0] }}:
  cron.{{ old_cron_state }}:
    - name: {{ renew_cert_cmd }} {{ domainlist|join(' ') }}
    - month: '*'
    - minute: '{{ letsencrypt.cron.minute }}'
    - hour: '{{ letsencrypt.cron.hour }}'
    - dayweek: '{{ letsencrypt.cron.dayweek }}'
    - identifier: letsencrypt-{{ setname }}-{{ domainlist[0] }}
    - require:
      - cmd: create-initial-cert-{{ setname }}-{{ domainlist | join('+') }}
      {% if letsencrypt.install_method == 'package' %}
      - pkg: letsencrypt-client
      {% else %}
      - file: {{ renew_cert_cmd }}
      {% endif %}

create-fullchain-privkey-pem-for-{{ setname }}:
  cmd.run:
    - name: |
        cat {{ letsencrypt.config_dir.path }}/live/{{ setname }}/fullchain.pem \
            {{ letsencrypt.config_dir.path }}/live/{{ setname }}/privkey.pem \
            > {{ letsencrypt.config_dir.path }}/live/{{ setname }}/fullchain-privkey.pem && \
        chmod 600 {{ letsencrypt.config_dir.path }}/live/{{ setname }}/fullchain-privkey.pem
    - creates: {{ letsencrypt.config_dir.path }}/live/{{ setname }}/fullchain-privkey.pem
    - require:
      - cmd: create-initial-cert-{{ setname }}-{{ domainlist | join('+') }}

{% endfor %}
