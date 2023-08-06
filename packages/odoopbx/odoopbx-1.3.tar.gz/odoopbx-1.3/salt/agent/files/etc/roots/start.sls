asterisk_agent_start:
  module.run:
    - name: odoo.execute
    - model: asterisk_common.settings
    - method: on_agent_start
    - args: []
