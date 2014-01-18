#!/usr/bin/python

import sys
import json
import MySQLdb as mdb
import matplotlib as mpl
from matplotlib.dates import DateFormatter, HourLocator, DayLocator
mpl.use('Agg')
import matplotlib.pyplot as plt

days = DayLocator()
hours = HourLocator()
dayFormatter = DateFormatter('%d/%m/%y')      

def printfig(x, y, label, filename):

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.ylabel(label)
    plt.xticks(rotation=70)
    plt.xlabel('Date')
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_minor_locator(hours)
    ax.xaxis.set_major_formatter(dayFormatter)
    plt.tick_params(axis='both', which='major', labelsize=8)
    plt.savefig(filename, format='png')

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
	    printfig(dates, tweets, 'Tweets', pathname+'/tweets.png')

	    # print sentiment
	    printfig(dates, sentiment, 'Average Sentiment', pathname+'/sentiment.png')


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

