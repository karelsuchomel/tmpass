#!/bin/bash

pipe=/dev/shm/tmpass_pipe
log_folder=/var/tmpass

sudo mkdir -p $log_folder
sudo cp tmpass.service /etc/systemd/system/
sudo cp tmpass.sh /etc/profile.d/
sudo cp tmpass.py /usr/sbin/

