{% from "agent/map.jinja" import agent with context %}

agent-service-files:
  file.recurse:
    - name:  /etc/systemd/system/
    - source: salt://agent/files/systemd/
    - template: jinja
    - context: {{ agent }}
    - require:
        - agent-pip-reqs

agent-service-enable:
  service.enabled:
    - names:
        - salt-master
        - salt-api
        - salt-minion
    - require:
        - agent-service-files

{%- if agent.running %}
agent-service-running:
  service.running:
    - names:
        - salt-master
        - salt-api
        - salt-minion
    - require:
        - agent-service-files
{%- endif %}
