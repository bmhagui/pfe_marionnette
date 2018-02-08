#!/bin/bash

echo " "
echo "Run the following commands: "
echo "python tracking/Tentacle/server.py "
echo "runSofa ArticulatedTentacle_LeapControl.py"
echo " "

python tracking/Tentacle/server.py &
runSofa ArticulatedTentacle_LeapControl.pyscn

ps aux | grep "server.py" | grep -v grep | awk {'print $2'} | xargs kill
