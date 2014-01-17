#!/bin/sh

# Set up system for TweetAnalysis tools

# Do this before running this script
# install git
# sudo apt-get install git
# get code
# git clone https://github.com/benjamingarzon/TweetAnalysis.git

# You need a credentials file as described in findTweets.py
# Just set the same password and run this script

PASSWORD="ronald21"
USER="tweetuser"
DBNAME="tweetsdb"

# update
sudo apt-get update

# install apache
sudo apt-get install apache2

# install mysql
sudo apt-get install mysql-server

# install python packages
sudo apt-get install python-pip
sudo apt-get install python-MySQLdb
sudo pip install oauth2


# open remote connections
sudo sed -i.bak -e s/127.0.0.1/0.0.0.0/g /etc/mysql/my.cnf
sudo service mysql restart 

# create database and table
echo "DROP DATABASE IF EXISTS $DBNAME;" > commands.sql
echo "CREATE DATABASE $DBNAME;" >> commands.sql
echo "CREATE user '$USER'@'localhost' IDENTIFIED BY '$PASSWORD';" >> commands.sql
echo "CREATE user '$USER'@'%' IDENTIFIED BY '$PASSWORD';" >> commands.sql
echo "GRANT ALL ON $DBNAME.* TO '$USER'@'localhost';" >> commands.sql
echo "GRANT ALL ON $DBNAME.* TO '$USER'@'%';" >> commands.sql
echo "QUIT" >> commands.sql

mysql -u root -p < commands.sql

echo "USE $DBNAME;" > commands.sql
echo "DROP TABLE IF EXISTS tweets;" >> commands.sql
echo "CREATE TABLE tweets (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, date DATETIME, lon FLOAT, lat FLOAT, message VARCHAR(140));" >> commands.sql
echo "QUIT" >> commands.sql

mysql -u $USER -p"$PASSWORD" < commands.sql
rm commands.sql

# create website
cd TweetAnalysis
mkdir web
sudo cp /etc/apache2/sites-available/default /etc/apache2/sites-available/webstats
sudo sed -i.bak -e 's#/var/www#~/TweetAnalysis/web#g' /etc/apache2/sites-available/webstats
sudo a2dissite default && sudo a2ensite webstats
sudo service apache2 restart

echo "Done"

