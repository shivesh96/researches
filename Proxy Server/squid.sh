echo "***Cybolite Squid Proxy Installer***"
echo "Updating System...."
sudo apt update -y && apt upgrade -y
echo "Installing Proxy"
read -p "Set Proxy Port : " proxy_port
echo -e "Selected Port:\n$proxy_port"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
sudo apt install squid -y && apache2-utils -y
sudo ufw allow OpenSSH
sudo ufw allow Squid
sudo ufw allow $proxy_port
# sudo ufw allow 3128
echo "Enabling Firewall..."
sudo ufw enable
echo "Firewall Enabled..."

echo "Adding Authentication..."
read -p "Enter Username : " username
sudo htpasswd -c /etc/squid/passwords $username
#read -p "Enter Password : " userpass
echo "Configuring Squid to port 3128"
echo "Add 'cache deny all' just before 'http_access deny all'"
echo "change 'http_access deny all' to 'http_access allow all' just after line '#  And finally deny all other access to this proxy'"
echo `
  include /etc/squid/conf.d/*
  auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwords
  auth_param basic realm proxy
  acl authenticated proxy_auth REQUIRED
  # Example rule allowing access from your local networks.
  acl localnet src your_ip_address
  # Adapt localnet in the ACL section to list your (internal) IP networks
  # from where browsing should be allowed
  http_access allow localnet
  http_access allow localhost
  http_access allow authenticated
  # And finally deny all other access to this proxy
  http_access deny all
  `
echo "opening file..."
sleep 5
sudo nano /etc/squid/squid.conf
#sed -i 's/http_access deny all/http_access allow all/' /etc/squid/squid.conf
echo "Reloading Services, Please wait..."
sudo ufw reload
sudo systemctl restart squid.service
sudo systemctl status squid.service

curl -v -x username:userpass@127.0.0.1:3128 https://www.google.com/
echo "Done"


#sed -i 's/# And finally deny all other access to this proxy\nhttp_access deny all/http_access allow all/g' squid.cong
