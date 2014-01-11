#!/bin/sh

# set up system for TweetAnalysis tools
# you need a credentials file as described in findTweets.py
# and set up the these environment variables with the same values

PASSWORD=
USER="tweetuser"
DBNAME="tweetsdb"

# update
sudo apt-get update

# install git
sudo apt-get install git

# install mysql
sudo apt-get install mysql-server

# install python packages
sudo apt-get install python-pip
sudo apt-get install python-MySQLdb
sudo pip install oauth2

# get code
git clone https://github.com/benjamingarzon/TweetAnalysis.git

# create database and table
echo "DROP DATABASE IF EXISTS $DBNAME;" > commands.sql
echo "CREATE DATABASE $DBNAME;" >> commands.sql
echo "CREATE user '$USER'@'localhost' IDENTIFIED BY '$PASSWORD';" >> commands.sql
echo "USE $DBNAME;"  >> commands.sql
echo "GRANT ALL ON $DBNAME.* TO '$USER'@'%';" >> commands.sql
echo "QUIT" >> commands.sql

mysql -u root -p < commands.sql

echo "USE $DBNAME;" > commands.sql
echo "DROP TABLE IF EXISTS tweets;" >> commands.sql
echo "CREATE TABLE tweets (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, day INT, month VARCHAR(5), year INT, time VARCHAR(20), lon FLOAT, lat FLOAT, message VARCHAR(150));" >> commands.sql
echo "QUIT" >> commands.sql

mysql -u $USER -p"$PASSWORD" < commands.sql

rm commands.sql

echo "Done"

