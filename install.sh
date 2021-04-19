#!/bin/bash
mongod &
cd frontend
ng build --prod
cd ../backend
pipenv --three
pipenv install
pipenv shell
python -m src.seeds