
# Proxy Using Docker

### Install Squid and Run as docker demon
    docker run -d --name squid-proxy -p 3128:3128 sameersbn/squid:latest

#### /etc/squid/squid.conf
    http_port 0.0.0.0:3128  # Or any specific IP you want to allow

### Install Privoxy and Run as docker demon
    docker run -d --name privoxy -p 8118:8118 haugene/privoxy:latest

#### /etc/privoxy/config
    listen-address 0.0.0.0:8118 #  Or any specific IP you want to allow

## Indtall Proxychains on Main Machine
    sudo apt update
    sudo apt install proxychains

#### /etc/proxychains.conf
    dynamic_chain
    chain_len = 1
    tcp_read_time_out 15000
    tcp_connect_time_out 8000

# Add the Squid and Privoxy Docker container IP addresses and port numbers
    [ProxyList]
    socks5 127.0.0.1 9050   # For Tor
    http 127.0.0.1 8118     # For Privoxy
    # socks5 127.0.0.1 3128   # For Squid

## Install TOR
    sudo apt install tor

#### /etc/tor/torrc
    SocksPort 9050

### ALLOW PORTS
    sudo ufw allow 3128/tcp
    sudo ufw allow 8118/tcp
    sudo ufw allow 9050/tcp

## RESTART
    docker restart squid-proxy
    docker restart privoxy
    service tor restart

# RUN
    proxychains curl http://www.example.
    



### Add local proxy to web proxy
    worker_processes 400; # or you can adjust according to your system conf
    http {
        upstream proxychains {
            server 127.0.0.1:8118
        }
    }
    server {
        listen 80;
        server_name example.com;

        location / {
            proxy_pass http://proxychains;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            # Other proxy configuration settings
        }
    }


# Load balancing
    http {
        upstream myapp {
            ip_hash;
            server backend1.example.com;
            server backend2.example.com;
            server 192.168.1.200;
            server 192.168.1.12;
            server localhost:3128;
        }
    }





### Auto calculate worker_processes
    worker_processes auto;

    http {
        # Calculate the number of CPU cores or threads
        init_by_lua '
            local nproc = io.popen("nproc"):read("*n")
            worker_processes = nproc
        ';

        # Rest of your NGINX configuration
        ...
    }

- The worker_processes directive is initially set to "auto."

- In the init_by_lua block, the nproc command is used to obtain the number of CPU cores or threads available on the server. This value is assigned to the worker_processes variable.

- The rest of your NGINX configuration follows as usual.

