#!/bin/bash

set -ueo pipefail

print_help() {
	echo "Edit the folders to backup in the script and then run the script from the backup folder (that is to say, cd to it)"
	echo "options"
	echo "    -z | --zip to pack folders into zip files"
}

init_sd_card() {
	external_storage=0
	for path in $(adb -d shell ls /storage)
	do
		if [ "$path" != "emulated" ] && [ "$path" != "self" ] && [ "$path" != "sdcard0" ]; then
			external_storage="storage/$path"
		elif [[ "$path" == *"-"* ]]; then
			external_storage="storage/$path"
		fi
	done
	if [ "$external_storage" -eq 0 ]; then
		echo "no SD card found"
	else
		echo "SD card found"
	fi
}

create_zips=0
while [[ "$#" -gt 0 ]]; do
	case $1 in
		-z|--zip) create_zips=1; ;;
		-h|--help) print_help; ;;
		*) echo "Unknown parameter: $1" ;;
	esac
	shift
done

adb devices > /dev/null

internal_storage="/sdcard"
init_sd_card
internal_backup_dir="internal"
external_backup_dir="external"
INTERNAL_DIRS=("Music" "Download" "Documents" "DCIM" "Pictures" "Recordings")
EXTERNAL_DIRS=()

zip_extension=".zip"

# this opens adb bash shell, but we no longer need it, I just want to note the command
# adb shell -t bash -i

echo "directories to backup (* are on SD card):"

echo "" 
for path in "${INTERNAL_DIRS[@]}"
do
	echo "- $path"
done
if [ "$external_storage" != 0 ]; then
	for path in "${EXTERNAL_DIRS[@]}"
	do
		echo "* $path"
	done
fi
echo ""

echo "pulling files from the device..."
mkdir -p "$internal_backup_dir" && cd "$internal_backup_dir" || exit 1
for path in "${INTERNAL_DIRS[@]}"
do
true
	adb -d pull "$internal_storage/$path"
done
cd ..
if [ "$external_storage" != 0 ]; then
	mkdir -p "$external_backup_dir" && cd "$external_backup_dir" || exit 1
	for path in "${EXTERNAL_DIRS[@]}"
	do
		adb -d pull "$external_storage/$path"
	done
fi
cd ..

if [ "$create_zips" -eq 1 ]; then
	echo ""
	echo "creating archives..."
	cd "$internal_backup_dir"
	for path in "${INTERNAL_DIRS[@]}"
	do
		if [ -d "$path" ]; then
			zip "$path$zip_extension" "$path" > /dev/null && rm -rf "$path" && echo "created: $path$zip_extension"
		fi
	done
	if [ "$external_storage" != 0 ]; then
		cd "../$external_backup_dir"
		for path in "${EXTERNAL_DIRS[@]}"
		do
			if [ -d "$path" ]; then
				zip "$path$zip_extension" "$path" > /dev/null && rm -rf "$path" && echo "created: $path$zip_extension"
			fi
		done
	fi
fi

echo ""
echo "finished"
