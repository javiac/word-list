# Word list application using Python, Flask, MongoDB, Angular and Angular Material.
## Features:
- Search anagrams
- Persistent sorting
- Create, update and delete words
- Dependency injection keeps one single connection to the database

![Selección_344](https://user-images.githubusercontent.com/8288832/115359701-38e09580-a1bf-11eb-9058-75cf38aa4fb3.png)

# Installation

    git clone git@github.com:javiac/word-list.git
    cd word-list

## Backend

### Database (Install MongoDB)
    mongod --version
    // Output: db version v4.4.5
    sudo mkdir /data
    sudo mkdir /data/db
    sudo chmod 777 /data/db

### Run mongod in a new terminal
    mongod

### Install Python dependencies and insert seeds
    sudo apt install python3-pip
    pip3 install pipenv
    cd backend
    pipenv --three
    pipenv install
    pipenv shell
    python -m src.seeds
    // Output: Inserted  19
    chmod u+x start.sh

## Frontend
### Install NodeJs and npm using Node Version Manager
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
    export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")" [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
    // Check installation
    node --version
    // Should output something like: v14.15.1
    npm --version
    // Should output something like: 6.14.8
### Install frontend dependencies and build
    cd ../frontend
    npm install -g @angular/cli
    npm i
    ng build --prod

## Run the project
    cd ..
    chmod u+x start.sh
    ./start.sh

## Access the application 
### Angular development server
    http://localhost:4200/
### Flask application serving production ready copy of the project
    http://0.0.0.0:5000/


## Extra
### Connect to specific db
    export PATH=$PATH:~/.local/bin:/home/javi/mongosh-0.11.0-linux/bin
    mongosh "mongodb://localhost:27017/<db_name>"
