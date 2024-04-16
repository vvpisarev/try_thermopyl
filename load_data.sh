#!/bin/bash

# Name of the file containing the list of files to download
file_list="doi_list.txt"

# Base URL for the files
base_url="https://trc.nist.gov/ThermoML/"

# Directory to save the downloaded files
download_dir="./mixture_data/"
mkdir $download_dir

# Read each line in the file
while IFS= read -r line
do
	# HEADER=$(curl -I $URL)
	# echo $HEADER
	# FILENAME=$(echo $HEADER | grep -o -E 'filename=.*$' | sed -e 's/filename=//' | tr -d '\r')

	URL="${base_url}${line}.xml"
	SECOND_HALF=$(echo "$line" | cut -d'/' -f2)
	FILENAME="${SECOND_HALF}.xml"
	if [ -f "${download_dir}${FILENAME}" ]; then
    		echo "File $FILENAME exists."
	else
    		echo "File $FILENAME does not exist. Downloading..."
  		# Download the file using wget
  		wget -P "$download_dir" "$URL"
  		# wget -O "$FILENAME" -P "$download_dir" "$URL"
    		# curl -O $URL
	fi

done < "$file_list"

if [ -f "mixture_data/*.xml.*" ]; then
	ls mixture_data/*.xml.*
	rm mixture_data/*.xml.*
fi
