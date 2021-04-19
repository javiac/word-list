#!/bin/bash
mongod &
cd frontend
ng serve &
cd ../backend 
./start.sh