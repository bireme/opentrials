#!/bin/bash
sudo mysql -u root -p --execute="CREATE DATABASE opentrials; CREATE USER 'tester'@'localhost' IDENTIFIED BY 'puffpuff'; GRANT ALL PRIVILEGES ON opentrials.* TO 'tester'@'localhost';"

