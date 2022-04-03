#!/bin/bash

PIPE=/dev/shm/tmpass_pipe
LOG_FOLDER=/var/log/

echo `date`" - Login UID: "$UID >>$LOG_FOLDER/tmpass_login_notification.log

if [[ ! -p $PIPE ]]; then
    echo `date`" - Reader not running!" >>$LOG_FOLDER/tmpass_login_notification.log
else
    echo "$UID" >$PIPE
fi

