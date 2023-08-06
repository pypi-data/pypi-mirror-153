{% if salt['config.get']('security_reactor_enabled') %}

security-ipset-whitelist:
  ipset.set_present:
    - set_type: hash:net
    - name: whitelist
    - comment: True
    - counters: True

security-ipset-blacklist:
  ipset.set_present:
    - set_type: hash:net
    - name: blacklist
    - comment: True
    - counters: True

security-ipset-authenticated:
  ipset.set_present:
    - set_type: hash:ip
    - name: authenticated
    - comment: True
    - counters: True

security-ipset-banned:
  ipset.set_present:
    - set_type: hash:ip
    - name: banned
    - comment: True
    - counters: True
    - timeout: {{ salt['config.get']('security_banned_timeout', '3600') }}

security-ipset-expire_short:
  ipset.set_present:
    - set_type: hash:ip
    - name: expire_short
    - comment: True
    - counters: True
    - timeout: {{ salt['config.get']('security_expire_short_timeout', '30') }}

security-ipset-expire_long:
  ipset.set_present:
    - set_type: hash:ip
    - name: expire_long
    - comment: True
    - counters: True
    - timeout: {{ salt['config.get']('security_expire_long_timeout', '3600') }}

security-chan-voip:
  iptables.chain_present:
    - name: voip

security-ports-udp:
  iptables.insert:
    - position: 1
    - table: filter
    - family: ipv4
    - chain: INPUT
    - jump: voip
    - dports: {{ salt['config.get']('security_ports_udp') }}
    - proto: udp
    - comment: iax,sip

security-ports-tcp:
  iptables.insert:
    - position: 1
    - table: filter
    - family: ipv4
    - chain: INPUT
    - jump: voip
    - dports: {{ salt['config.get']('security_ports_tcp') }}
    - proto: tcp
    - comment: www,manager,sip,http

securityp-match-whitelist:
  iptables.insert:
    - chain: voip
    - match-set: whitelist src
    - jump: ACCEPT
    - position: 1

security-match-blacklist:
  iptables.insert:
    - chain: voip
    - match-set: blacklist src
    - jump: DROP
    - position: 2

securityp-match-authenticated:
  iptables.insert:
    - chain: voip
    - match-set: authenticated src
    - jump: ACCEPT
    - position: 3

securityp-match-banned:
  iptables.insert:
    - chain: voip
    - match-set: banned src
    - jump: DROP
    - position: 4

securityp-match-expire_short:
  iptables.insert:
    - chain: voip
    - match-set: expire_short src
    - jump: ACCEPT
    - position: 5

securityp-match-expire_long:
  iptables.insert:
    - chain: voip
    - match-set: expire_long src
    - jump: DROP
    - position: 6

{% for agent in ['VaxSIPUserAgent', 'friendly-scanner', 'sipvicious', 'sipcli'] %}
security-scanner-{{ agent }}:
  iptables.append:
    - chain: voip
    - match: string
    - string: {{ agent }}
    - algo: bm
    - jump: DROP
{% endfor %}

{% endif %}
