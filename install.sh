#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root."
    exit
fi

if [ "$#" -ne 1 ]
then
    echo "Missing first param."
    echo "Usage: "$0" <UID>"
    echo "<UID> ... UID of managed user"
    exit
fisyhf

# Create environment file
echo 'TMPASS_MNG_USER='$1 | tee -a /etc/systemd/system/tmpass_environment
echo 'TMPASS_SLEEP=3600' | tee -a /etc/systemd/system/tmpass_environment

cp tmpass.service /etc/systemd/system/
cp tmpass_login_notification.sh /etc/profile.d/
cp tmpass.py /usr/sbin/
cp dateToFourDigits.py /usr/sbin/
chmod +x /usr/sbin/tmpass.py /usr/sbin/dateToFourDigits.py

touch /var/log/tmpass_login_notification.log
chmod 666 /var/log/tmpass_login_notification.log
echo `date`" - installed" >>/var/log/tmpass_login_notification.log

systemctl enable tmpass.service
systemctl restart tmpass.service
