#!/bin/bash

# Function to trim spaces from input
trim() {
    echo "$1" | xargs
}

# Function to check if input is a valid comma-separated list of numbers
validate_input() {
    local input="$1"
    # Validate if input only contains numbers separated by commas
    if [[ "$input" =~ ^[0-9]+(,[0-9]+)*$ ]]; then
        return 0
    else
        return 1
    fi
}

# Extract available rule numbers from UFW
get_available_rules() {
    sudo ufw status numbered | grep -Eo '^\s*\[ *[0-9]+\]' | tr -d '[] ' | sort -n
}

# Show UFW status with numbers
sudo ufw status numbered

# Get available UFW rule numbers
available_rules=($(get_available_rules))

# Check if there are no rules available
if [[ ${#available_rules[@]} -eq 0 ]]; then
    echo "No UFW rules available to delete."
    exit 1
fi

echo "Available UFW rule numbers: ${available_rules[*]}"

# Ask for input in comma-separated format
read -p "Enter the rule numbers you want to delete (comma-separated): " input

# Trim input and validate it
input=$(trim "$input")

# Validate input format
if ! validate_input "$input"; then
    echo "Invalid input! Please provide a valid comma-separated list of integers."
    exit 1
fi

# Convert comma-separated input into an array
IFS=',' read -r -a rules <<< "$input"

# Remove duplicates from user input
unique_rules=($(echo "${rules[@]}" | tr ' ' '\n' | sort -u))

# Check if any input rules were provided
if [[ ${#unique_rules[@]} -eq 0 ]]; then
    echo "No valid rule numbers provided."
    exit 1
fi

# Validate that all input rules exist in the available UFW rules
invalid_rules=()
valid_rules=()
for rule in "${unique_rules[@]}"; do
    if [[ "$rule" =~ ^[0-9]+$ ]]; then
        if [[ " ${available_rules[*]} " =~ " $rule " ]]; then
            valid_rules+=("$rule")
        else
            invalid_rules+=("$rule")
        fi
    else
        invalid_rules+=("$rule")
    fi
done

# If there are invalid rules, show a message and continue with valid ones
if [[ ${#invalid_rules[@]} -gt 0 ]]; then
    echo "The following rule numbers are invalid or do not exist: ${invalid_rules[*]}"
fi

# If there are no valid rules, exit
if [[ ${#valid_rules[@]} -eq 0 ]]; then
    echo "No valid rules to delete."
    exit 1
fi

# Sort valid rules in descending order to avoid conflicts during deletion
sorted_rules=($(for i in "${valid_rules[@]}"; do echo "$i"; done | sort -nr))

# Confirm with the user before proceeding
echo "The following rules will be deleted: ${sorted_rules[*]}"
read -p "Are you sure you want to proceed? (y/n): " confirm
if [[ "$confirm" != "y" ]]; then
    echo "Operation canceled."
    exit 0
fi

# Delete each valid rule one by one without confirmation
for rule in "${sorted_rules[@]}"; do
    echo "Deleting rule number: $rule"
    yes | sudo ufw delete "$rule"
done

echo "UFW rules deleted successfully."