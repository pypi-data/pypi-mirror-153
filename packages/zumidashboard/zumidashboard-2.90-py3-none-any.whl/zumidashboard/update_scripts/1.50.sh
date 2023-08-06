#!/bin/sh

sudo mv /home/pi/Zumi_Content /home/pi/Dashboard/
sudo chown -R pi /home/pi/Dashboard/Zumi_Content
sudo systemctl disable jupyter.service
sudo mkdir /home/pi/.jupyter/custom
cat > /home/pi/.jupyter/custom/custom.js << EOF
window.addEventListener('unload', function(){
  // For Firefox
  IPython.notebook.session.delete();
});
window.onbeforeunload = function(){
  // For Chrome
  IPython.notebook.session.delete();
};
EOF

# added for backup
mkdir /home/pi/Dashboard/user
mkdir /home/pi/Dashboard/user/User1
mv /home/pi/log_v* /home/pi/Dashboard/user/User1
cp -r /home/pi/Dashboard/Zumi_Content /home/pi/Dashboard/user/User1
mkdir /home/pi/Dashboard/user/User1//My_Projects
mkdir /home/pi/Dashboard/user/User1//My_Projects/Jupyter
mkdir /home/pi/Dashboard/user/User1//My_Projects/Blockly
sudo chown -R pi /home/pi/Dashboard/user
sudo rm -rf /home/pi/Dashboard/DriveImg
cp -r /home/pi/Dashboard/user/User1 /home/pi/Dashboard/backup