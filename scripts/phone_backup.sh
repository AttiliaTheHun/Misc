#!/bin/bash

echo "Note that the creation of the archives as well as the recreation into zip archives can take MINUTES. Be patient!"
echo ""

set -ueo pipefail

tar2zip=1
remove_originals=1
while [[ "$#" -gt 0 ]]; do
	case $1 in
		-z|--tar2zip) tar2zip=1; shift ;;
		-r|--cleanup) remove_originals=1; shift ;;
		*) echo "Unknown parameter: $1" ;;
	esac
	shift
done

adb devices > /dev/null

sdcard="/sdcard"
DIRS=("Music" "Documents" "DCIM" "Pictures" "Recordings")
tar_extension=".tar.gz"
zip_extension=".zip"

# this opens abd bash shell, but we no longer need it
# adb shell -t bash -i

echo "directories to backup:"
# create the scripts to send over to adb
adb_script="cd $sdcard"
adb_cleanup_script="cd $sdcard" 
for path in "${DIRS[@]}"
do
	adb_script="${adb_script};tar -czf $path$tar_extension $path"
	adb_cleanup_script="${adb_cleanup_script};rm $path$tar_extension"
	echo "- $path"
done

echo ""

adb_script="${adb_script};exit"
adb_cleanup_script="${adb_cleanup_script};exit"

echo "creating archives..."
echo "$adb_script" | adb shell

echo ""
echo "pulling archives from the device..."
for path in "${DIRS[@]}"
do
true
	adb pull "$sdcard/$path$tar_extension"
done

echo ""
echo "removing archives from the device..."
echo "$adb_cleanup_script" | adb shell #2> /dev/null

# Convert a tar file into a zip file by repacking the files
if [ "$tar2zip" == 1 ]; then
	echo ""
	echo "converting TAR archives to ZIP archives..."
	for path in "${DIRS[@]}"
	do
		if [ -e "$path$tar_extension" ]; then
			tar -xzf "$path$tar_extension"
			zip -r "$path$zip_extension" "$path" > /dev/null && echo "created: $path$zip_extension" && rm -rf "$path" || echo "failed to create: $path$zip_extension" 
			test "$remove_originals" -eq 1 && rm "$path$tar_extension"
		fi
	done
fi

echo ""
echo "finished"
