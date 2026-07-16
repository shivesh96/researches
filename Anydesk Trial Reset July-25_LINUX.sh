#!/bin/bash

echo "Stopping AnyDesk..."
pkill -f anydesk

echo "Removing AnyDesk config and cache..."
sudo rm -rf ~/.anydesk
sudo rm -rf ~/.cache/anydesk
sudo rm -f ~/.config/anydesk
sudo rm -f ~/.config/AnyDesk
sudo rm -f ~/.local/share/anydesk
sudo rm -f ~/.local/share/AnyDesk
sudo rm -f ~/.config/autostart/anydesk.desktop

echo "Removing AnyDesk system-level configs (if installed via package)..."
sudo rm -rf /etc/anydesk
sudo rm -rf /var/lib/anydesk
sudo rm -f /usr/share/applications/anydesk.desktop

echo "AnyDesk trial data reset complete."