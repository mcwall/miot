# miot
MiOT - My Internet of Things

# Installation
install node / npm
`npm install -g ask-cli`
`ask init --no-browser`

install ngrok
`ngrok authtoken <token>`

install pip requirements
`python3 -m venv py-env`
`source py-env/bin/activate`
`pip install -r requirements.txt`

running
`tools/tunnel_init.sh`
`tools/app_init.sh`

startup
`su - pi -c "/home/pi/miot/tools/tunnel_init.sh"`
`su - pi -c "/home/pi/miot/tools/app_init.sh"`
