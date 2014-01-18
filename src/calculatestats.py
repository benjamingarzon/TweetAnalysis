#!/usr/bin/python

import sys
import json
import MySQLdb as mdb
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def getstats(filename, pathname):

    # get credentials
    with open(filename) as credfile:
        credentials = json.load(credfile)

	try:
            conn = mdb.connect(credentials['host'], credentials['user'], credentials['pwd'], credentials['database']);
            c = conn.cursor()
            c.execute("SELECT date, COUNT(*), AVG(sentiment) FROM sentiments GROUP BY DATE(date), HOUR(date);" )
            rows = c.fetchall()
	    columns = zip(*rows)

            # get info
	    dates = columns[0]
	    tweets = columns[1]
	    sentiment = columns[2]
	    #print dates
	    #print counts

	    # print tweets
	    plt.clf()
    	    plt.plot(dates, tweets, label="Tweets")
	    plt.ylabel('Tweets')
            plt.xticks(rotation=70)
	    plt.xlabel('Date')
            plt.tick_params(axis='both', which='major', labelsize=8)
            plt.tick_params(axis='both', which='minor', labelsize=6)
    	    plt.savefig(pathname+'/tweets.png', format='png')

	    # print sentiment
	    plt.clf()
    	    plt.plot(dates, sentiment, label="Sentiment")
	    plt.ylabel('Average sentiment')
            plt.xticks(rotation=70)
	    plt.xlabel('Date')
            plt.tick_params(axis='both', which='major', labelsize=8)
            plt.tick_params(axis='both', which='minor', labelsize=6)
    	    plt.savefig(pathname+'/sentiment.png', format='png')


        except mdb.Error, e:
  
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
    
        finally:    
        
            if conn:    
                 conn.close()


def main():

    filename = sys.argv[1]
    pathname = sys.argv[2]

    # getstats from table
    getstats(filename, pathname)
               
if __name__ == '__main__':
    main()    

