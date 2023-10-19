echo "***Cybolite Squid Proxy Installer***"
echo "Updating System...."
sudo apt update -y && apt upgrade -y
echo "Installing Proxy"
read -p "Set Proxy Port : " proxy_port
echo -e "Selected Port:\n$proxy_port"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
sudo apt install squid3
echo "Enabling Firewall..."
sudo ufw enable
echo "Configuring Squid to port 3128"
sudo ufw allow OpenSSH
udo ufw allow Squid
#allow $proxy_port
sudo ufw allow 3128
echo "Add 'cache deny all' just before 'http_access deny all'"
echo "change 'http_access deny all' to 'http_access allow all' just after line '#  And finally deny all other access to this proxy'"
echo "opening file..."
sleep 5
sudo nano /etc/squid/squid.conf
#sed -i 's/http_access deny all/http_access allow all/' /etc/squid/squid.conf
echo "Reloading Services, Please weit..."
sudo ufw reload
sudo systemctl restart squid.service
sudo systemctl status squid.service
echo "Done"


#sed -i 's/# And finally deny all other access to this proxy\nhttp_access deny all/http_access allow all/g' squid.cong
