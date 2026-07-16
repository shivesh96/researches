#!/bin/bash

# Define text colors and formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display colored text
color_echo() {
  local color=$1
  local message=$2
  echo -e "${color}${message}${NC}"
}

# Update and upgrade
color_echo $YELLOW "Updating package list and upgrading packages..."
sudo apt update && sudo apt upgrade -y
color_echo $GREEN "Update and upgrade completed successfully."

# Install Docker and Docker Compose
color_echo $YELLOW "Installing Docker and Docker Compose..."
sudo apt install docker.io docker-compose -y
color_echo $GREEN "Docker and Docker Compose installation completed."

# Install Tor and Torsocks
color_echo $YELLOW "Installing Tor and Torsocks..."
sudo apt install tor torsocks -y
color_echo $GREEN "Tor and Torsocks installation completed."

# Additional instructions for Torify, Proxychains, and more can be added here

color_echo $GREEN "Script execution finished."


# Function to add or update a configuration line in torrc
add_to_torrc() {
  local config_line="$1"
  if grep -q "$config_line" /etc/tor/torrc; then
    color_echo $GREEN "Config line already exists: $config_line"
  else
    echo "$config_line" | sudo tee -a /etc/tor/torrc > /dev/null
    color_echo $GREEN "Added config line: $config_line"
  fi
}

# Add or update the configuration lines
add_to_torrc "SafeSocks 1"
add_to_torrc "TestSocks 1"
add_to_torrc "CircuitBuildTimeout 2"
add_to_torrc "KeepalivePeriod 2"
add_to_torrc "NewCircuitPeriod 15"
add_to_torrc "NumEntryGuards 8"

# Restart Tor to apply the new settings
sudo systemctl restart tor

color_echo $GREEN "Tor configuration updated and Tor has been restarted."
