#!/bin/bash
if ! [ -x "$(command -v php)" ]; then
  echo 'Error: php is not installed.' >&2
  brew install php
fi

current_php_version=$(php -v | head -n 1 | cut -d " " -f 2)
echo "Current PHP version is $current_php_version"
current_php_fpm_version=$(php-fpm -v | head -n 1 | cut -d " " -f 2)
echo "Current PHP-FPM version is $current_php_fpm_version" # /usr/local/opt/php@7.4/sbin/php-fpm -v

# ask for new php version
echo "Enter new PHP version: (7.1|7.3|7.4|8.0|8.1|8.2)"
read new_php_version

# sphp 8.3
sphp new_php_version
exit

echo "Checking if PHP Version $new_php_version is installed..."

if [ ! -d "/usr/local/opt/php@$new_php_version" ]; then
    echo "PHP Version $new_php_version is not installed"
    
    echo "Checking if HomeBrew is installed"
    if ! [ -x "$(command -v brew)" ]; then
        echo 'Error: brew is not installed.' >&2
        exit 1
    fi

    echo "Installing php@$new_php_version"
    brew install php@$new_php_version
else
    echo "PHP Version $new_php_version is already installed"
    # brew reinstall php@$new_php_version
fi

echo "Switching to PHP Version $new_php_version ..."

echo "Unlinking current PHP $current_php_version Version"
brew unlink php@$current_php_version

echo "Linking PHP Version $new_php_version"
brew link --force --overwrite php@$new_php_version

# echo "Rechecking PHP Version $new_php_version"
# brew unlink php@$current_php_version && brew link --force php@$new_php_version

echo "::::::Setting up environment::::::::::"

# check if /usr/local/opt/php@$new_php_version directory exists and is linked
if [ ! -d "/usr/local/opt/php@$new_php_version" ]; then
    echo "PHP Version $new_php_version is not installed"
    exit 1
fi

bin_path=$(echo "/usr/local/opt/php@$new_php_version/bin")
sbin_path=$(echo "/usr/local/opt/php@$new_php_version/sbin")

echo "Checking if $bin_path exists in ~/.zshrc"
if grep -q "$bin_path" ~/.zshrc; then
    echo "PHP Version $new_php_version is already set in ~/.zshrc"
    echo "Removing PHP Version $new_php_version from ~/.zshrc"
    sed -i '' "/$bin_path/d" ~/.zshrc
fi

grep -v "export PATH=/usr/local/opt/php@" ~/.zshrc > /tmp/.zshrc.tmp && mv /tmp/.zshrc.tmp ~/.zshrc

echo "export PATH=$bin_path:"'$PATH' >> ~/.zshrc
echo "export PATH=$sbin_path:"'$PATH' >> ~/.zshrc

export LDFLAGS="-L/usr/local/opt/php@$new_php_version/lib"
export CPPFLAGS="-I/usr/local/opt/php@$new_php_version/include"

echo "::::::Config File::::::::::"
echo "/usr/local/etc/php/$new_php_version/php-fpm.d/www.conf"

echo "::::::Restarting PHP@$new_php_version::::::::::"
brew services restart php@$new_php_version
zsh
# brew services list
# /usr/local/opt/php@7.3/sbin/php-fpm --nodaemonize

