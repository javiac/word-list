#Installation
sudo apt install python3-pip
pip3 install pipenv
npm install -g @angular/cli
./install.sh
./start.sh

#Extra
##Connect to plytix db
export PATH=$PATH:~/.local/bin:/home/javi/mongosh-0.11.0-linux/bin
mongosh "mongodb://localhost:27017/plytix"
