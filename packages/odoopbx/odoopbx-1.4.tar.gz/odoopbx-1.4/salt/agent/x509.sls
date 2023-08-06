agent-x509-ssl-cert-group:
  group.present:
    - name: ssl-cert
    - system: True

agent-x509-pki-dir:
  file.directory:
    - name: /etc/pki/selfsigned
    - group: ssl-cert
    - mode: 2750
    - makedirs: True

agent-x509-private-key:
  x509.private_key_managed:
    - name: /etc/pki/selfsigned/privkey.pem
    - mode: 0640
    - require:
      - agent-x509-pki-dir

agent-x509-certificate:
  x509.certificate_managed:
    - name: /etc/pki/selfsigned/fullchain.pem
    - signing_private_key: /etc/pki/selfsigned/privkey.pem
    - CN: "{{grains['id']}}"
    - basicConstraints: "critical CA:true"
    - keyUsage: "critical digitalSignature, keyEncipherment"
    - subjectKeyIdentifier: hash
    - authorityKeyIdentifier: keyid,issuer:always
    - days_valid: 36500
    - days_remaining: 0
    - require:
      - agent-x509-private-key
    - creates:
      - /etc/pki/selfsigned/fullchain.pem

agent-x509-symlink:
  file.symlink:
    - name: /etc/pki/current
    - target: /etc/pki/selfsigned
    - creates: /etc/pki/current
