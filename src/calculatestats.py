#!/usr/bin/python

import sys
import json
import MySQLdb as mdb
import matplotlib.pyplot as plt

def getstats(filename):

    # get credentials
    with open(filename) as credfile:
        credentials = json.load(credfile)

	try:
            conn = mdb.connect(credentials['host'], credentials['user'], credentials['pwd'], credentials['database']);
            c = conn.cursor()
            c.execute("SELECT HOUR(date), COUNT(*) FROM tweets GROUP BY HOUR(date);" )
            rows = c.fetchall()

            # get info
	    dates = list()
	    counts = list()

	    for row in rows:
		dates.append(row[0])
		counts.append(row[1])

	    print dates
	    print counts

	    plt.clf()
    	    plt.plot(dates, counts, label="ValueF")
            #plt.legend(['Fund', 'Market'])
    	    plt.ylabel('Counts')
            #plt.xticks(rotation=70)
	    plt.xlabel('Date')
            #plt.tick_params(axis='both', which='major', labelsize=8)
            #plt.tick_params(axis='both', which='minor', labelsize=6)
    	    plt.savefig("stats.png", format='png')

        except mdb.Error, e:
  
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
    
        finally:    
        
            if conn:    
                 conn.close()


def main():

    filename = sys.argv[1]
   
    # getstats from table
    getstats(filename)
               
if __name__ == '__main__':
    main()    

