#!/bin/bash

echo "Stopping AnyDesk..."
pkill -f AnyDesk

echo "Clearing AnyDesk data..."
rm -rf ~/Library/Application\ Support/AnyDesk
rm -f ~/Library/Preferences/com.anydesk.AnyDesk.plist
rm -rf ~/Library/Caches/com.anydesk.AnyDesk
rm -rf ~/Library/Logs/AnyDesk

echo "Reset complete. You can now reopen AnyDesk."