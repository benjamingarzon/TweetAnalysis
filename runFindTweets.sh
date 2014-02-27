#!/bin/bash


while true
do
  if pgrep findTweets.py > /dev/null ; then
      echo "process running"
  else
      src/findTweets.py $1 config/credentials.json 
  fi
  sleep 60
done
