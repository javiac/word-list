# Installation

## Backend
git clone git@github.com:javiac/word-list.git
### Database
Install MongoDB (at least 4.4)
sudo mkdir /data
sudo mkdir /data/db
sudo chmod 777 /data/db
### Server
sudo apt install python3-pip
pip3 install pipenv
cd backend
pipenv --three
pipenv install
pipenv shell
python -m src.seeds
chmod u+x start.sh

# Frontend
cd ../frontend
npm install -g @angular/cli
npm i
ng build --prod
cd ..

# Run
chmod u+x start.sh
./start.sh

# Extra
## Connect to plytix db
export PATH=$PATH:~/.local/bin:/home/javi/mongosh-0.11.0-linux/bin
mongosh "mongodb://localhost:27017/plytix"
