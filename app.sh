#!/bin/bash

cd /home/pi/miot
python3 -m venv py-env
source py-env/bin/activate
python www/app.py
