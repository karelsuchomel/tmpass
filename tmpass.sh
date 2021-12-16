#!/bin/bash

pipe=/dev/shm/tmpass_pipe
log_folder=/var/tmpass/

if [[ ! -p $pipe ]]; then
    echo "Reader not running -" `date` >>$log_folder/log
else
    echo "$UID" >$pipe
fi

