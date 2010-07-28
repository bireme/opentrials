#!/bin/bash
sudo mysql -u root -p --execute="CREATE DATABASE clinicaltrials; CREATE USER 'tester'@'localhost' IDENTIFIED BY 'puffpuff'; GRANT ALL PRIVILEGES ON clinicaltrials.* TO 'tester'@'localhost';"

