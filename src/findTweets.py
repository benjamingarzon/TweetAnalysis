#!/usr/bin/python
'''
Downloads tweets that contain a certain word and stores date, time, longitude, latitude and the message in a database

Usage: findTweets word credentials.json

WORD is the word that the tweets must

CREDENTIALS is a json file with the following information about the database and twitter authentication credentials

{"host":"XXXX", 
"user":"XXXX", 
"pwd": "XXXX", 
"database":"XXXX",
"access_token_key":"XXXX",
"access_token_secret":"XXXX",
"consumer_key":"XXXX",
"consumer_secret":"XXXX"}
'''

from __future__ import division
import sys
import json
import twitterstream
import MySQLdb as mdb
import time
import httplib
import urllib2

reload(sys)
sys.setdefaultencoding("utf-8")

def parseLine(word, line):
    ''' extract attributes from each tweet (line of the twitter stream) '''

    date, lon, lat, text = 0, 0, 0, None
    found = False
    d = json.loads(line)
    
    # search word in text field of the tweet
    if 'text' in d.keys():
        text = d[u'text'].encode('ascii', 'ignore').replace('\n',' ')
        if text.lower().find(word.lower()) >= 0:
            found = True
                    
            # extract information                
            if 'created_at' in d.keys():
                created = d[u'created_at']

		# do conversion to mysql datetime format
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created,'%a %b %d %H:%M:%S +0000 %Y'))
                
            if 'coordinates' in d.keys():
                coord = d[u'coordinates']
                if isinstance(coord, dict):
                    coord = coord[u'coordinates']
                    lon, lat = coord[0], coord[1]
                
    return ((date, lon, lat, text), found)

def fetchData(word, filename):
    ''' download tweets and insert attributes of those containing WORD in the database '''
    
    # get credentials
    
    with open(filename) as credfile:
        credentials = json.load(credfile) 
    
    # connect to db
    try:
        conn = mdb.connect(credentials['host'], credentials['user'], credentials['pwd'], credentials['database']);
        c = conn.cursor()

    except mdb.Error, e:
  
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    else:
        
	while 1:
        
            #download tweets
            url = "https://stream.twitter.com/1/statuses/sample.json"
            parameters = []

	    try: 	     
	        response = twitterstream.twitterreq(url, "GET", parameters, credentials)
	
	    except urllib2.HTTPError, e:
                print 'HTTPError = ' + str(e.code)
            except urllib2.URLError, e:
                print 'URLError = ' + str(e.reason)
            except httplib.HTTPException, e:
                print 'HTTPException'
	   
	    else:
        	# parse lines and insert info in db
        	for outrow, found in (parseLine(word, line) for line in response):
            	    if found:
		
                        outtext = '\t'.join(map(str, outrow))+"\n"
                        print outrow
                        c.execute("INSERT INTO tweets(date, lon, lat, message) VALUES (%s,%s,%s,%s)", outrow)
		        conn.commit()
    
    finally:    
        
        if conn:    
            conn.close()

    
def main():
    ''' fetch tweets containing WORD and save in database filename '''

    word = sys.argv[1]
    filename = sys.argv[2]
   
    # fetch the data
    fetchData(word, filename)
               
if __name__ == '__main__':
    main()
