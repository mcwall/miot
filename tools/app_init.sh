#!/bin/bash

cd /home/pi/miot

python3 -m venv py-env
source py-env/bin/activate
cd www
python app.py

exit 0
