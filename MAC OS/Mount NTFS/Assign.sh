#!/bin/bash

# Function to list NTFS drives
list_ntfs_drives() {
  echo "Detecting NTFS drives..."
  ntfs_drives=($(diskutil list | grep NTFS | awk '{print $NF}'))

  if [ ${#ntfs_drives[@]} -eq 0 ]; then
    echo "No NTFS drives detected."
    exit 1
  fi

  echo "Available NTFS drives:"
  for i in "${!ntfs_drives[@]}"; do
    echo "$((i + 1)). ${ntfs_drives[$i]}"
  done
}

# Function to get disk name and add to /etc/fstab
add_fstab_entry() {
  echo "Please select a disk by number:"
  read -r disk_number

  if ! [[ $disk_number =~ ^[0-9]+$ ]] || [ $disk_number -le 0 ] || [ $disk_number -gt ${#ntfs_drives[@]} ]; then
    echo "Invalid selection."
    exit 1
  fi

  selected_disk="${ntfs_drives[$((disk_number - 1))]}"

  # Add entry to /etc/fstab
  echo "Adding NTFS write access for $selected_disk to /etc/fstab"
  sudo sh -c "echo 'LABEL=$selected_disk none ntfs rw,auto,nobrowse' >> /etc/fstab"

  echo "Entry added. Unmounting and remounting $selected_disk"
  sudo diskutil unmount /dev/$selected_disk
  sudo diskutil mount /dev/$selected_disk

  echo "Done. You can now access your NTFS drive with read/write permissions."
}

# Main script
list_ntfs_drives
add_fstab_entry