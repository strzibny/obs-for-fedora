#!/bin/sh
# Convert an rc script to regular bin file
sed -i -e "s|^.*rc.status.*$||" $1
sed -i -e "s|^.*rc_reset.*$||" $1
sed -i -e "s|^.*rc_exit.*$||" $1

