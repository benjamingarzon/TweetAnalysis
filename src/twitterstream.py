import oauth2 as oauth
import urllib2 as urllib

_debug = 0

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the credentials above from a file.
Requires a file with the credentials in this format
{"access_token_key":"XXXX",
"access_token_secret":"XXXX",
"consumer_key":"XXXX",
"consumer_secret":"XXXX"}

'''
def twitterreq(url, method, parameters, credentials):

  access_token_key = credentials['access_token_key']
  access_token_secret = credentials['access_token_secret']
  consumer_key = credentials['consumer_key']
  consumer_secret = credentials['consumer_secret']

  oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
  oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    print line.strip()

def tweetsearch(term):
  url = "https://api.twitter.com/1.1/search/tweets.json?q=%s"%(term)
  print url
  parameters = []
  response = twitterreq(url, "GET", parameters)
  return response

if __name__ == '__main__':
  fetchsamples()

