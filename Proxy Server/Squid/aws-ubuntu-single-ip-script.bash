#!/bin/bash
PORT="3128"
USER="DORA"
PASS="DORA"
REALM="proxy"
apt update
apt install -y squid apache2-utils
cat > /etc/squid/squid.conf <<EOL
# safe ports
acl SSL_ports port 443
acl Safe_ports port 80          # http
acl Safe_ports port 21          # ftp
acl Safe_ports port 443         # https
acl Safe_ports port 70          # gopher
acl Safe_ports port 210         # wais
acl Safe_ports port 1025-65535  # unregistered ports
acl Safe_ports port 280         # http-mgmt
acl Safe_ports port 488         # gss-http
acl Safe_ports port 591         # filemaker
acl Safe_ports port 777         # multiling http
acl CONNECT method CONNECT

# passwd auth
auth_param digest program /usr/lib/squid/digest_file_auth -c /etc/squid/passwd.htdigest
auth_param digest children 5
auth_param digest realm ${REALM}
acl authenticated proxy_auth REQUIRED

# define access
http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports
http_access allow localhost manager
http_access deny manager
http_access allow authenticated
http_access deny all
http_port ${PORT}

# disable all logging
access_log none
cache_store_log none
cache_log /dev/null

# disable caching
cache deny all

# hide squid version in error pages


# ???
coredump_dir /var/spool/squid
# ???
refresh_pattern ^ftp:           1440    20%     10080
refresh_pattern ^gopher:        1440    0%      1440
refresh_pattern -i (/cgi-bin/|\?) 0     0%      0
refresh_pattern (Release|Packages(.gz)*)$      0       20%     2880
refresh_pattern .               0       20%     4320

# Make this proxy anonymous, it will make all services think 
# it is the originating IP of the requests
via off
forwarded_for off
request_header_access Allow allow all
request_header_access Authorization allow all
request_header_access WWW-Authenticate allow all
request_header_access Proxy-Authorization allow all
request_header_access Proxy-Authenticate allow all
request_header_access Cache-Control allow all
request_header_access Content-Encoding allow all
request_header_access Content-Length allow all
request_header_access Content-Type allow all
request_header_access Date allow all
request_header_access Expires allow all
request_header_access Host allow all
request_header_access If-Modified-Since allow all
request_header_access Last-Modified allow all
request_header_access Location allow all
request_header_access Pragma allow all
request_header_access Accept allow all
request_header_access Accept-Charset allow all
request_header_access Accept-Encoding allow all
request_header_access Accept-Language allow all
request_header_access Content-Language allow all
request_header_access Mime-Version allow all
request_header_access Retry-After allow all
request_header_access Title allow all
request_header_access Connection allow all
request_header_access Proxy-Connection allow all
request_header_access User-Agent allow all
request_header_access Cookie allow all
request_header_access All deny all
EOL
digest="$( printf "%s:%s:%s" "$USER" "$REALM" "$PASS" | md5sum | awk '{print $1}' )"
printf "%s:%s:%s\n" "$USER" "$REALM" "$digest" > /etc/squid/passwd.htdigest
service squid restart