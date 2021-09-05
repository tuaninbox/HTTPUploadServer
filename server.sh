#!/bin/bash
source /opt/HTTPUploadServer/env/bin/activate
export FLASK_DIR=$(pwd)
export FLASK_APP=/opt/HTTPUploadServer/appsimple
if [[ $1 == *":"* ]]; then
	host=$(echo $1 | cut -f1 -d":")
	port=$(echo $1 | cut -f2 -d":")
elif [[ $1 ]]; then
	echo "Usage: $0 <IP Address>:<port>"
	exit 1
else
	host="0.0.0.0"
	port=80
fi
echo "Working directory is $FLASK_DIR"
flask run -h $host -p $port
