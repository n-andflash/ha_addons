#!/bin/sh

ADDON_FILE=sds_wallpad.py
OPTION_FILE=options_standalone.json
GENERATE_OPTION_SCRIPT=generate_options_standalone.py

if which sudo >/dev/null; then
	SUDO=sudo
else
	SUDO=
fi

if which apk >/dev/null; then
	$SUDO apk update
	$SUDO apk add --no-cache python3 py3-pip
	python3 -m pip install --upgrade pip
	python3 -m pip install pyserial paho-mqtt
elif which apt-get >/dev/null; then
	$SUDO apt-get update
	$SUDO apt-get install -y python3 python3-pip
	$SUDO apt-get install -y python3-serial python3-paho-mqtt
fi


if [ ! -f $OPTION_FILE ]; then
	python3 $GENERATE_OPTION_SCRIPT $OPTION_FILE
	echo "$OPTION_FILE is generated! please modify it then start this script again."
	exit 1
fi

python3 $ADDON_FILE $OPTION_FILE
