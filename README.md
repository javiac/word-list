sudo apt install python3-pip
pip3 install pipenv
cd backend; pipenv --three
export PATH=$PATH:~/.local/bin:/home/javi/mongosh-0.11.0-linux/bin
mongod
mongosh
./backend/start.sh
cd ./frontend; ng build --watch


pipenv shell


npm install -g @angular/cli

Connect to plytix db
mongosh "mongodb://localhost:27017/plytix"