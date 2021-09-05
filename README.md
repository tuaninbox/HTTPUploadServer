# HTTPUploadServer
A Web Server for download and upload file

## Installation
### Without Virtual Envinronment
- pip install -r requirements.txt

### With Virtual Environment
- mkdir env
- python -m venv env
- source env/bin/activate
- pip install -r requirements.txt

## Download
- Access http://<$IP Address of server>:<$port>

## Upload
- Access http://<$IP Address of server>:<$port>/up

## Upload Using CURL
- curl -X Post -F "file=@<$filename>" http://<$IP Address of server>:<$port>/uper
- curl -F "file=@<$filename>" http://<$IP Address of server>:<$port>/uper
