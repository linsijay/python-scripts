'''
simple script to connect solr and delete data
'''

import urllib, urllib2

USERNAME = 'tester'
PASSWORD = '123456789'
ENDPOINT = 'http://127.0.0.1:8080/solr/update?%s' % (urllib.urlencode({'commit':'true'}))
QUERY_FILTER = 'logTime:[2013-03-01T16:00:00.000Z TO 2013-03-24T16:00:00.000Z]'

if __name__ == "__main__":
    # for DIGEST auth-method
    passwdmngr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passwdmngr.add_password('auth', ENDPOINT, USERNAME, PASSWORD)
    authhandler = urllib2.HTTPDigestAuthHandler(passwdmngr)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    
    req = urllib2.Request(ENDPOINT)
    req.add_header('Content-Type', 'text/xml; charset=utf-8')
    req.add_data('<delete><query>{0}</query></delete>'.format(QUERY_FILTER))
    
    response = urllib2.urlopen(req, timeout=600)
    print response.read()
