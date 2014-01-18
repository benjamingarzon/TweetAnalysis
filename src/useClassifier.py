#!/usr/bin/python
import pickle
import sys
import json
import MySQLdb as mdb
import classfunctions as cf


def classify(classfilename, credfilename, stopfilename, featurefilename):
    # get stop words and feature list
    stopWords = cf.getStopWordList(stopfilename)
    featureList = cf.getFeatureList(featurefilename)

    # Pickle classifier
    print "Loading classifier"
    inp = open(classfilename, 'rb')
    NBClassifier = pickle.load(inp)
    inp.close()

    # get credentials
    with open(credfilename) as credfile:
        credentials = json.load(credfile)

        try:
	    print "Connecting to database"
            conn = mdb.connect(credentials['host'], credentials['user'], credentials['pwd'], credentials['database']);
            c = conn.cursor()
            c.execute("SELECT tweets.id, tweets.date, message FROM tweets LEFT JOIN sentiments2 ON tweets.id = sentiments.id WHERE sentiments.id IS NULL;" )
            rows = c.fetchall()

	    # classify each tweet and save result in sentiment db

	    for row in rows:
		tweetid = row[0]
		date = row[1] 
		message = row[2]
            	processedTestTweet = cf.processTweet(message)
        	featureVector = cf.getFeatureVector(processedTestTweet, stopWords)
        	features = cf.extract_features(featureVector, featureList)
        	sentiment = cf.transsent[NBClassifier.classify(features)]
	        c.execute("INSERT INTO sentiments (id, date, sentiment) VALUES (%s,%s,%s)", (tweetid, date, sentiment))

		print (tweetid, date, sentiment)

	    conn.commit()

        except mdb.Error, e:
  
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
    
        finally:    
        
            if conn:    
                 conn.close()


def main():

    classfilename = sys.argv[1]
    credfilename = sys.argv[2]
    stopfilename = sys.argv[3]
    featurefilename = sys.argv[4]

    # classify tweets
    classify(classfilename, credfilename, stopfilename, featurefilename)
               
if __name__ == '__main__':
    main()    





