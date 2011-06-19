import ConfigParser, getopt, os, sys, twitter, stackexchange 

USAGE = '''Usage: tweet StackOverflow#'''

so = stackexchange.Site(stackexchange.StackOverflow)
so_user = so.user(sys.argv[1:])

def PrintUsageAndExit():
    print USAGE
    sys.exit(2)
     
class TweetRc(object):
    def __init__(self):
        self._config = None
        
    def GetConsumerKey(self):
        return self._GetOption('consumer_key')
    
    def GetConsumerSecret(self):
        return self._GetOption('consumer_secret')
        
    def GetAccessKey(self):
        return self._GetOption('access_key')
        
    def GetAccessSecret(self):
        return self._GetOption('access_secret')       
       
    def _GetOption(self, option):
        try:
            return self._GetConfig().get('Tweet', option)
        except:
            return None
            
    def _GetConfig(self):
        if not self._config:
            self._config = ConfigParser.ConfigParser()
            self._config.read(os.path.expanduser('~/.tweetrc'))
        return self._config
       
def main():
    display_name = so_user.display_name
    reputation = so_user.reputation.format()
    message = "Stack Overflow User: " + display_name + "  Reputation: " + reputation
    rc = TweetRc()
    consumer_key = rc.GetConsumerKey()
    consumer_secret = rc.GetConsumerSecret()
    access_key = rc.GetAccessKey()
    access_secret = rc.GetAccessSecret()
    if not consumer_key or not consumer_secret or not access_key or not access_secret:
        print "Didn't successfully load .tweetrc"
    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                        access_token_key=access_key, access_token_secret=access_secret)
    try:
        status = api.PostUpdate(message)
    except UnicodeDecodeError:
        print "Your message could not be encoded. Perhaps it contains non-ASCII characters? "
        print "Try explictly specifying the encoding with the --encoding flag"
        sys.exit(2)
    print "%s just posted: %s" % (status.user.screen_name, status.text)
    
if __name__ == "__main__":
    main()
