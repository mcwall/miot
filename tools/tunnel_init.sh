#!/bin/bash

# Start a new ngrok tunnel
sudo pkill ngrok
$(ngrok http 5000 >> /dev/null &) & disown
sleep 20s

# Update ASK Skill to new URL
PUBLIC_URL=$(curl -s localhost:4040/api/tunnels | perl -pe 's|.*?public_url":"(https.*?)".*|\1|')
ask api get-skill --stage development -s amzn1.ask.skill.2f7bf966-7045-4f16-94b9-958c5d0b3cff > /tmp/ask-skill-old.json
cp /tmp/ask-skill-old.json /tmp/ask-skill-new.json
sed -i "s|https://.*ngrok\.io|$PUBLIC_URL|" /tmp/ask-skill-new.json
ask api update-skill --stage development -s amzn1.ask.skill.2f7bf966-7045-4f16-94b9-958c5d0b3cff -f /tmp/ask-skill-new.json

# Kill resource-hogging node in case it's still running
sudo pkill -kill node

exit 0