#!/bin/sh

# Set up system for TweetAnalysis tools on Ubuntu machine with username 'ubuntu'

# Do this before running this script
## install git
# sudo apt-get update
# sudo apt-get -y install git
## get code
# git clone https://github.com/benjamingarzon/TweetAnalysis.git

# You need a credentials file config/credentials.json as described in findTweets.py
# Just set the same password and run this script

WORD=""
PASSWORD=""
USER="tweetuser"
DBNAME="tweetsdb"

# update
sudo apt-get update

# install apache
sudo apt-get -y install apache2

# install mysql
sudo apt-get -y install mysql-server

# install python packages
sudo apt-get -y install python-pip
sudo apt-get -y install python-MySQLdb
sudo pip install oauth2
sudo apt-get -y install python-matplotlib
sudo apt-get -y install python-nltk
sudo apt-get -y install python-numpy


# open remote connections
sudo sed -i.bak -e s/127.0.0.1/0.0.0.0/g /etc/mysql/my.cnf
sudo service mysql restart 

# create database and tables
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

echo "DROP TABLE IF EXISTS sentiments;" >> commands.sql
echo "CREATE TABLE sentiments (id INT NOT NULL PRIMARY KEY, date DATETIME, sentiment INT);" >> commands.sql
echo "QUIT" >> commands.sql

mysql -u $USER -p"$PASSWORD" < commands.sql
rm commands.sql

# create website
cd TweetAnalysis
sudo cp /etc/apache2/sites-available/default /etc/apache2/sites-available/webstats
sudo sed -i.bak -e 's#/var/www#/home/ubuntu/TweetAnalysis/web#g' /etc/apache2/sites-available/webstats
sudo a2dissite default && sudo a2ensite webstats
sudo service apache2 restart

# download tweets
nohup src/findTweets.py $WORD config/credentials.json &

# schedule sentiment analysis and statistics for every hour
DIR=`pwd`
echo "0 * * * * cd $DIR; src/useClassifier.py data/classifier.pkl config/credentials.json data/stopwords.txt data/feature_list.txt; src/calculatestats.py config/credentials.json web" | crontab

echo "Done"

