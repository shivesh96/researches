read -p "Enter a word: " proxy_port
echo "Port Selected : $proxy_port"
echo "Add 'cache deny all' just before 'http_access deny all'"
echo "change 'http_access deny all' to 'http_access allow all'"
echo "Found in Line Numner: "
grep -n 'http_access deny all' squid.conf
sed -i 's/http_access deny all/cache deny all\nhttp_access allow all/' squid.conf


#sed -i 's/# And finally deny all other access to this proxy\nhttp_access deny all/http_access allow all/gm' squid.conf
