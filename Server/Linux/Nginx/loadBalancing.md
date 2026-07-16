```
upstream backend {
    ip_hash;
    # sticky; # Sticky sessions require the NGINX Plus version or a third-party module like NGINX Sticky Module.

    # Sticky session based on a custom cookie
    # sticky cookie srv_id expires=1h domain=yourdomain.com path=/;

    #server 127.0.0.1:80;  # Local server (adjust port if needed)
    server 13.200.103.154:80;  # Remote server (adjust domain/IP and port if needed)

    # Optionally, set weights for servers if you want to prioritize one
    #server 127.0.0.1:443 weight=1;
    #server 13.200.103.154:80 weight=2;
}

server {
    server_name test.railrestro.com;

    root /var/www/rr-front/public;
    index index.php;

    access_log /var/log/nginx/railrestro.com.access.log;
    error_log /var/log/nginx/railrestro.com.error.log;

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location / {
        proxy_pass http://backend;  # Pass requests to the load balancer upstream
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

#    location / {
#       try_files $uri $uri/ =404;
#    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/test.railrestro.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/test.railrestro.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
    listen 80;
    server_name test.railrestro.com;

    location / {
        return 301 https://$server_name$request_uri;
    }

```
