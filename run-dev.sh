#!/bin/sh

if [ ! -d "database" ]; then
	echo "Creating database directory..."
	mkdir database
fi
VENV_NAME=".venv-3.13-sh"

if [ ! -f "$VENV_NAME" ]; then
	echo "venv not exist, creating new one..."
	python -m venv $VENV_NAME
fi

echo "Activate venv"
$VENV_NAME/bin/activate

echo "Checking pip list"
python -m pip list

echo "Checking requirements file"

if [ -f "requirements.txt" ]; then
	echo "requirements file found, installing"
	python -m pip install -r requirements.txt
else
	echo "requirements file not found, skip instaling"
fi

IP="${1:127.0.0.1}"
PORT="8800"
URL=$IP+":"+$PORT

echo "$URL"
