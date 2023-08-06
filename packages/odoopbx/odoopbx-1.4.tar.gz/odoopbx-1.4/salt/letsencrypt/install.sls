# -*- coding: utf-8 -*-
# vim: ft=sls
{%- from "letsencrypt/map.jinja" import letsencrypt with context %}

{#- Use empty default for `grains.osfinger`, which isn't available in all distros #}
{%- if letsencrypt.install_method == 'package' and
       grains.osfinger|d('') == 'Amazon Linux-2' %}
{%-   set rhel_ver = '7' %}
letsencrypt_external_repo:
  pkgrepo.managed:
    - name: epel
    - humanname: Extra Packages for Enterprise Linux {{ rhel_ver }} - $basearch
    - mirrorlist: https://mirrors.fedoraproject.org/metalink?repo=epel-{{ rhel_ver }}&arch=$basearch
    - enabled: 1
    - gpgcheck: 1
    - gpgkey: https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-{{ rhel_ver }}
    - failovermethod: priority
    - require_in:
      - pkg: letsencrypt-client
{%- endif %}

{%- if letsencrypt.install_method == 'package' and grains.os|d('') == 'CentOS' %}
letsencrypt-epel-releasehttps://github.com/XeryusTC/letsencrypt-formula.git:
  pkg.installed:
    - pkgs:
        - epel-release
    - require_in:
      - pkg: letsencrypt-client
{%- endif %}

letsencrypt-client:
  {%- if letsencrypt.install_method == 'package' %}
    {%- set pkgs = letsencrypt.pkgs or [letsencrypt._default_pkg] %}
  pkg.installed:
    - pkgs: {{ pkgs | json }}
  {%- elif letsencrypt.install_method == 'git' %}
  pkg.installed:
    - name: {{ letsencrypt.git_pkg }}
  {%-   if letsencrypt.version is defined and letsencrypt.version|length %}
  git.cloned:
    - name: https://github.com/certbot/certbot
    - branch: {{ letsencrypt.version }}
    - target: {{ letsencrypt.cli_install_dir }}
  {%-   else %}
  git.latest:
    - name: https://github.com/certbot/certbot
    - target: {{ letsencrypt.cli_install_dir }}
    - force_reset: True
  {%-   endif %}
  {%- elif letsencrypt.install_method == 'pip' %}
  pkg.installed:
    - pkgs: {{ letsencrypt.virtualenv_pkg | json }}
  virtualenv.managed:
    - name: {{ letsencrypt.cli_install_dir }}
    - python: python3
    - pip_pkgs:
  {%-   if letsencrypt.version is defined and letsencrypt.version|length %}
      - certbot=={{ letsencrypt.version }}
  {%-   else %}
      - certbot
  {%-   endif %}
  {%-   for pkg in letsencrypt.pip_pkgs %}
      - {{ pkg }}
  {%-   endfor %}
  {%- endif %}
    - reload_modules: True
