#!/bin/bash

# Function to remove fstab entries related to NTFS
cleanup_fstab() {
  echo "Cleaning up NTFS entries from /etc/fstab..."
  sudo sed -i.bak '/ntfs/d' /etc/fstab
  echo "Cleanup completed. Backup of original file is saved as /etc/fstab.bak."
}

# Function to remount NTFS drives as read-only
remount_ntfs_readonly() {
  ntfs_drives=($(diskutil list | grep NTFS | awk '{print $NF}'))
  
  if [ ${#ntfs_drives[@]} -eq 0 ]; then
    echo "No NTFS drives detected."
    exit 1
  fi
  
  for disk in "${ntfs_drives[@]}"; do
    echo "Remounting $disk as read-only..."
    sudo diskutil unmount /dev/$disk
    sudo diskutil mount readOnly /dev/$disk
  done

  echo "All NTFS drives remounted as read-only."
}

# Main script
cleanup_fstab
remount_ntfs_readonly