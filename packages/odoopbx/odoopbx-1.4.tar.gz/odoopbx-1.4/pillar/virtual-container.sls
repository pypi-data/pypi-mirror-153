postgres:
  bake_image: True
nginx:
  service:
    opts:
      onlyif:
        - runlevel
asterisk:
    manager_bindaddr: 0.0.0.0
    http_tlsbindaddr: 0.0.0.0
