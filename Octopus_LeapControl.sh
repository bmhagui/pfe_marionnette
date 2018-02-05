#!/bin/bash
echo " "
echo "Run the following commands: "
echo "python server.py "
echo "runSofa Octopus_LeapControl.pyscn"
echo " "

python /home/sofa/Documents/pfe_marionnette/tracking/Octopus/server.py &
sudo /home/sofa/sofa/build/bin/runSofa Octopus_LeapControl.pyscn

ps aux | grep "server.py" | grep -v grep | awk {'print $2'} | xargs kill
