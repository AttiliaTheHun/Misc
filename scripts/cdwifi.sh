#!/bin/bash
# normally this thing need not exist and you woul run cdwifi.py directly, but for some reason my DNS settings are not getting updated when I connect to this particular WiFi,
# so I am changing them manually. At least they taught me this at the uni lol

on=0
help=0

while [[ "$#" -gt 0 ]]; do
    case $1 in
        on) on=1; shift ;;
		off) on=0; shift ;;
		-h|--help) help=1; shift ;;
        *) echo "Unknown parameter passed: $1" ;;
    esac
    shift
done

if [ $help == 1 ]; then
	echo "Use arg 'on' if you are connecting to CDWiFi and 'off' if you are no longer connecting to CDWiFi"
	echo "Be sure to run this with sudo as it needs to change DNS settings"
	exit 0
fi

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

if [ $on == 1 ]; then
	echo "nameserver 172.16.22.1" > /etc/resolv.conf
	python cdwifi.py
else
	printf "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf
fi
