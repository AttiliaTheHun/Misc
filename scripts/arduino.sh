#!/bin/bash

#set -ueo pipefail

cd ~
ARDUINO_MOUNT=("/dev/ttyACM0" "/dev/ttyACM1" "/dev/ttyACM2")

launch=1
help=0
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -p|--permissions) launch=0; shift ;;
        -h|--help) help=1; shift ;;
        *) echo "Unknown parameter passed: $1" ;;
    esac
    shift
done

if [ $help == 1 ]; then
	echo "Use -p to set arduino device read/write permissions without launching the IDE"
	exit 0
fi

mount_found=0
for path in "${ARDUINO_MOUNT[@]}"
do
	if [ -e "$path" ]; then
		sudo chmod a+rw "$path"
		echo "permissions changed successfully"
		echo "arduino found at $path"
		mount_found=1
	fi
done

if [ $mount_found == 0 ]; then
	echo "arduino not mounted"
fi

if [ $launch == 1 ]; then
	./Downloads/arduino-ide_2.3.4_Linux_64bit.AppImage
fi
