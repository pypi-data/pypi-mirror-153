asterisk:
  force_update: True
  lookup:
    rev: certified/16.8-cert12

letsencrypt:
  install_method: pip
  cli_install_dir: /srv/certbot
  config_dir:
    group: ssl-cert
    mode: 2755
  config:
    #server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: webmaster@odoopbx.com
    authenticator: webroot
    webroot-path: /var/spool/letsencrypt
    post-hook: chmod -R g+rX /etc/letsencrypt

nginx:
  lookup:
    server_available: /etc/nginx/conf.d
    server_enabled: /etc/nginx/conf.d
  install_from_repo: true
  package:
    opts: {}
  snippets:
    letsencrypt.conf:
      - location ^~ /.well-known/acme-challenge/:
          - root: /var/spool/letsencrypt
          - default_type: "text/plain"
    proxy_headers.conf:
      - proxy_set_header: Host $http_host
      - proxy_set_header: X-Real-IP $remote_addr
      - proxy_set_header: X-Forwarded-For $proxy_add_x_forwarded_for
      - proxy_set_header: X-Forwarded-Host $host
      - proxy_set_header: X-Forwarded-Proto $scheme
    websocket.conf:
      - proxy_http_version: 1.1
      - proxy_set_header: Upgrade $http_upgrade
      - proxy_set_header: Connection "upgrade"
    auth.conf:
      - satisfy: any
      - allow: 127.0.0.1
      - deny: all
      - auth_basic: Restircted
      - auth_basic_user_file: /etc/nginx/htpasswd
      # You may use 'htpasswd -c /etc/nginx/.htpasswd admin' from apache2-utils

  server:
    opts: {}
    config:
      worker_processes: 1
      worker_rlimit_nofile: 1024
      events:
        worker_connections: 1024
      http:
        sendfile: 'on'
        server_tokens: 'off'
        types_hash_max_size: 1024
        types_hash_bucket_size: 512
        server_names_hash_bucket_size: 64
        server_names_hash_max_size: 512
        keepalive_timeout: 65
        tcp_nodelay: 'on'
        gzip: 'on'
        gzip_http_version: '1.0'
        gzip_proxied: 'any'
        gzip_min_length: 500
        gzip_types:
          text/plain text/xml text/css text/comma-separated-values text/javascript
          application/json application/xml application/x-javascript
          application/javascript application/atom+xml
        proxy_redirect: 'off'
        proxy_buffers: '32 4k'
        proxy_buffer_size: 1k
        proxy_busy_buffers_size: 8k
        proxy_max_temp_file_size:  2048m
        proxy_temp_file_write_size:  64k
        proxy_cache_path: /tmp/nginx levels=1:2 keys_zone=one:10m inactive=60m
  servers:
    purge_servers_config: False
    managed:
      odoopbx.conf:
        enabled: true
        config:
          - server:
              - listen:
                  - '443 ssl'
              - ssl_certificate: /etc/pki/current/fullchain.pem
              - ssl_certificate_key: /etc/pki/current/privkey.pem
              - client_max_body_size: 1G
              - include:
                  - 'snippets/proxy_headers.conf'
              - location /:
                  - proxy_pass: http://localhost:8069
                  - add_header: X-Static no
                  - proxy_buffering: 'off'
                  - proxy_intercept_errors: 'on'
                  - proxy_headers_hash_bucket_size: 63
              - location /longpolling:
                  - proxy_pass: http://localhost:8072
              - location /ws:
                  - proxy_pass: http://localhost:8088/ws
                  - include:
                      - 'snippets/websocket.conf'
                      - 'snippets/proxy_headers.conf'
              - location /console:
                  - proxy_pass: http://agent:30000
                  - rewrite /console(.*) /$1 break
                  - include:
                      - 'snippets/websocket.conf'
                      - 'snippets/proxy_headers.conf'
      default.conf:
        enabled: true
        config:
          - server:
              - server_name: localhost
              - listen:
                  - '80 default_server'
              - include:
                  - 'snippets/letsencrypt.conf'
              - location /:
                  - return: 301 https://$host$request_uri

