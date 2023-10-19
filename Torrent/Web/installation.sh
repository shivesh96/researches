sudo add-apt-repository ppa:transmissionbt/ppa
sudo apt-get update
sudo apt-get install transmission-gtk transmission-cli transmission-common transmission-daemon
sudo service transmission-daemon stop

# "rpc-whitelist": "127.0.0.1,192.168.*.*",
sudo nano /var/lib/transmission-daemon/info/settings.json
sudo service transmission-daemon start


#http:127.0.01:9091/transmission

# Uninstallation
# sudo apt remove transmission*