{{ saltenv }}:
  '*':
    - odoopbx
    - local
    - ignore_missing: True
  'G@virtual_subtype:*':
    - virtual-container
  'G@init:systemd':
    - systemd
