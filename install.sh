#!/bin/bash

cd /home/pi/miot
python3 -m venv py-env
source py-env/bin/activate
pip install -r requirements.txt
