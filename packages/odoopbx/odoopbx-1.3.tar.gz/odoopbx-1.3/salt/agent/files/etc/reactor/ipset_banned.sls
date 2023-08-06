{% if data.data.get('RemoteAddress') %}
ipset-add-banned:
  local.cmd.run:
    - tgt: {{ data.id }}
    - args:
        - cmd: >
            ipset add -exist banned {{ data.data.RemoteAddress.split('/')[2] }}
            comment "{{ data.data.get('Service') ~ ' ' ~ data.data.get('Event') }}
            {{ data.data.get('AccountID') }}"

log-banned:
  local.log.warning:
    - tgt: {{ data.id }}
    - args:
        - message: >
            IP {{ data.data.RemoteAddress.split('/')[2] }} banned.
            {{ data.data.get('Service') ~ ' ' ~ data.data.get('Event') }}
            {{ data.data.get('AccountID') }}

ipset-del-expire_long:
  local.cmd.run:
    - tgt: {{ data.id }}
    - args:
        - cmd: >
            ipset del -exist expire_long {{ data.data.RemoteAddress.split('/')[2] }}
{% endif %}