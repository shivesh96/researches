docker network create mynetwork
docker run -d --name myproxy --network mynetwork -p 8080:80 nginx
docker run -d --name myproxy --network mynetwork -p 8080:80 -e http_proxy=http://your_proxy_username:your_proxy_password@your_proxy_server:your_proxy_port -e https_proxy=http://your_proxy_username:your_proxy_password@your_proxy_server:your_proxy_port nginx
docker run --rm --network mynetwork curl http://example.com
docker run -d --name myproxy --network mynetwork -p 8081:80 -e http_proxy=http://your_proxy_username:your_proxy_password@your_proxy_server:your_proxy_port -e https_proxy=http://your_proxy_username:your_proxy_password@your_proxy_server:your_proxy_port nginx


docker run -d --name myproxy --network mynetwork -p 8081:80 -e http_proxy=http://your_proxy_username:your_proxy_password@your_proxy_server:your_proxy_port -e https_proxy=http://your_proxy_username:your_proxy_password@your_proxy_server:your_proxy_port nginx
docker run -d --name myproxy --network mynetwork -p 8080:80 -e http_proxy=http://your_proxy_username:your_proxy_password@your_proxy_server:your_proxy_port -e https_proxy=http://your_proxy_username:your_proxy_password@your_proxy_server:your_proxy_port nginx
docker run --rm --network mynetwork curl http://example.com



docker-compose up
docker-compose up -d
docker stats
docker ps
docker ps -a

docker exec -it your_container_name_or_id composer install
docker exec -it myproxy /bin/bash


docker-compose down
docker stop myapp

docker run -d -p 8080:8080 --name myapp myapp
docker rm myapp


sudo service docker restart
sudo service docker status
docker-compose restart nginx