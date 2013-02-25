##Live Twitter - live stream of tweets on google map

![Alt text](twitter-live-screenshot.jpg "Live Tweets on google map")


* [Live Oscars Tweets recorded](http://cgtal.com/eras/live-twitter/live-twitter-oscars2.mp4) Feb 24 2013

==============

It shows the lastest 10 locations on google map in real time as they are being tweeted.

It uses gevent-socketio to push data to the client from the server.


##Installation

1. create a virtual environment folder next to README.md. Let's call it venv:
virtualenv venv

2. Install Python 2.7 if you don't have it.
in Ubuntu:
sudo apt-get intall python

3. apt-get install libevent-dev

4. activate the virtual environment
source venv/bin/activate

5. Install the following:
pip install gevent-socketio httplib2 oauth2 twitter

6. Make a twitter app online:
Go to http://dev.twitter.com
Sign in
Go to username>applications
Create a new one

7. make twitterstream/private.py to have your Twitter app settings:
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

8. Also put your search criteria in track variable and port in port variable

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


9. Run serve.py

10. open your browser and go to: http://0.0.0.0:8080/ or any port you chose

11. enjoy!


This is tested on Ubuntu 12.04
Check the requirements.txt for further details.


Cheers,
Eras
