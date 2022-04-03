#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root."
    exit
fi

# Delete environment file
rm /etc/systemd/system/tmpass_environment

systemctl disable tmpass.service

rm /etc/systemd/system/tmpass.service
rm /etc/profile.d/tmpass_login_notification.sh
rm /usr/sbin/tmpass.py
rm /usr/sbin/dateToFourDigits.py

rm /dev/shm/tmpass_pipe

rm /var/log/tmpass_login_notification.log
rm /var/log/tmpass_core.log
