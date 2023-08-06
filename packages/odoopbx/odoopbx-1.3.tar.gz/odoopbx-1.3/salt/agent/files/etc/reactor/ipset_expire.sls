{% if data.data.get('RemoteAddress') %}
ipset-add-expire_short:
  local.cmd.run:
    - tgt: {{ data.id }}
    - args:
        - cmd: >
            ipset add -quiet expire_short
            {{ data.data.RemoteAddress.split('/')[2] }}
            comment "{{ data.data.get('Service') ~ ' ' ~ data.data.get('Event') }}
            {{ data.data.get('AccountID') }}"
        - ignore_retcode: True

ipset-add-expire_long:
  local.cmd.run:
    - tgt: {{ data.id }}
    - args:
        - cmd: >
            ipset add -exist expire_long
            {{ data.data.RemoteAddress.split('/')[2] }}
            comment "{{ data.data.get('Service') ~ ' ' ~ data.data.get('Event') }}
            {{ data.data.get('AccountID') }}"
{% endif %}
