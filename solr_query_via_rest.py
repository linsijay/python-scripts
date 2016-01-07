'''
simple script to access solr
'''

import urllib, urllib2

USERNAME = 'tester'
PASSWORD = '123456789'
ENDPOINT = 'http://127.0.0.1:8080/solr/core/select?'
QUERY_FILTER = 'logTime:[2013-03-01T16:00:00.000Z TO 2013-03-24T16:00:00.000Z]'
OUTPUT_FORMAT = 'json' # csv, xml

if __name__ == "__main__":
    # for DIGEST auth-method
    passwdmngr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passwdmngr.add_password('auth', ENDPOINT, USERNAME, PASSWORD)
    authhandler = urllib2.HTTPDigestAuthHandler(passwdmngr)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    
    urldata = urllib.urlencode("wt=%s&%s" % (OUTPUT_FORMAT, QUERY_FILTER))
    req = urllib2.Request(url, urldata)  
    
    try:
        response = urllib2.urlopen(req, timeout=300)
        if OUTPUT_FORMAT == 'json':
            response = json.load(response)
        elif OUTPUT_FORMAT == 'csv':
            pass
        else:
            response = response.read()
    except:
        error_type, error_msg, error_obj = sys.exc_info()
        print 'Reason: %s, Detail: %s' % (error_type.__name__, error_msg)
    
    print response