"""
live twitter v 0.1
Display live tweets on google map

written by Erasmose  Feb 2013
https://github.com/erasmose/

Part of code based on Twitter example of gevent-socketio

You need to make a private.py and put your Twitter app account details there. 
In order to get Twitter app account:
Make a twitter app online:
Go to http://dev.twitter.com
Sign in
Go to username>applications
Create a new one

Example of a sample private.py:
#---------------------------------

# these tokens are necessary for user authentication
consumer_key = "falshdOIHDsdlksnsd"
consumer_secret = "aslkfdjHLlKSNFDlksnadlLLFNS"
access_key = "islhdals-asedlfhsLLSFDIHWLFLSKDNLSDHFLS"
access_secret = "aehfialhdfOIFDHSLWSHDLSHdhLSDHSLDHSLHDHDLSHDLSH"

# These are keywords to search for in the tweets:
track = "oscar,oscars,awards,academyawards"

# the port of this server:
port = 8080
#---------------------------------
"""
from private import port, track, consumer_key,consumer_secret,access_key,access_secret


from gevent import monkey; monkey.patch_all()
import gevent
#import tweetstream
import getpass

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace


from twitter import *




# create twitter API object
auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)
stream = TwitterStream(auth = auth, secure = True)






def broadcast_msg(server, ns_name, event, *args):
    pkt = dict(type="event",
               name=event,
               args=args,
               endpoint=ns_name)

    for sessid, socket in server.sockets.iteritems():
        socket.send_packet(pkt)


def send_tweets(server):

    # iterate over tweets matching this filter text
    # IMPORTANT! this is not quite the same as a standard twitter search
    #  - see https://dev.twitter.com/docs/streaming-api
    tweet_iter = stream.statuses.filter(track = track)


    for tweet in tweet_iter:
        # check whether this is a valid tweet
        if tweet.get('text') and tweet.get('geo'):
        
            # yes it is! print out the contents, and any URLs found inside
            print "(%s) @%s %s" % (tweet["created_at"], tweet["user"]["screen_name"], tweet["text"])
            print tweet['geo']['coordinates']
            for url in tweet["entities"]["urls"]:
                print " - found URL: %s" % url["expanded_url"]

            tweet['coord_x']=tweet['geo']['coordinates'][0]
            tweet['coord_y']=tweet['geo']['coordinates'][1]
            broadcast_msg(server, '/tweets', 'tweet', tweet)
            print "=="*10

    #stream = tweetstream.SampleStream(user, password)
    #for tweet in stream:
        





class Application(object):
    def __init__(self):
        self.buffer = []

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/') or 'index.html'

        if path.startswith('static/') or path == 'index.html':
            try:
                data = open(path).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".swf"):
                content_type = "application/x-shockwave-flash"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'/tweets': BaseNamespace})
        else:
            return not_found(start_response)


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


if __name__ == '__main__':

    print 'Listening on port http://0.0.0.0:%s' % port
    print "press Ctrl+c to stop the server\n"
    print "if it is not showing anything and no error is displayed,\nthen nobody is tweeting about what you are searching for."
    print "give it some time or change your search subject(s) that are in private.py in track string"
    
    server = SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843))
    gevent.spawn(send_tweets, server)
    server.serve_forever()
