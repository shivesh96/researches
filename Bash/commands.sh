# Set Default File Permissions For New Folders
find /path/to/your/app -type d -exec chmod 755 {} \;
find . -type d -exec chmod 755 {} \;

# Set Default File Permissions For New Files
find /path/to/your/app -type f -exec chmod 644 {} \;
find . -type f -exec chmod 644 {} \;


chmod -R 775 /path/to/your/app/storage
chmod -R 775 /path/to/your/app/bootstrap/cache
