{% if data.data.get('RemoteAddress') %}
ipset-add-authenticated:
  local.cmd.run:
    - tgt: {{ data.id }}
    - args:
        - cmd: >
            ipset add -exist authenticated
            {{ data.data.RemoteAddress.split('/')[2] }}
            comment "{{ data.data.get('Service') ~ ' ' ~ data.data.get('Event') }}
            {{ data.data.get('AccountID') }}"

ipset-del-expire_long:
  local.cmd.run:
    - tgt: {{ data.id }}
    - args:
        - cmd: >
            ipset del -exist expire_long {{ data.data.RemoteAddress.split('/')[2] }}
{% endif %}