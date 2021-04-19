#!/bin/bash
sudo mongod &
cd frontend
ng serve &
cd ../backend 
./start.sh