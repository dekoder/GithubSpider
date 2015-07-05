'''
Created on Jul 4, 2015

@author: Tommi Unruh
'''

import requests as r
import sys
import json

class Crawler(object):
    '''
    classdocs
    '''

    # constants
    OAUTH = {
        "token": "71cc84f627fd38b6d7a2e2ba7daf6792578982d9",
        }
    
    
    
    LINK_API   = "https://api.github.com"
    LINK_SEARCH_API = LINK_API + "/search/repositories"
    LINK_RATE_LIMIT = LINK_API + "/rate_limit"
    HEADER_USER_AGENT    = "tommiu@web.de"
    HEADER_XRATELIMIT_LIMIT     = "X-RateLimit-Limit"
    HEADER_XRATELIMIT_REMAINING = "X-RateLimit-Remaining"
    HEADER_AUTHORIZATION = "token %s" % OAUTH["token"] 
    
    HEADERS = {
            'User-Agent':    HEADER_USER_AGENT,
            'Authorization': HEADER_AUTHORIZATION,
            }
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def crawlSearching(self, q="language:PHP", sort=None, order=None):
        per_page = 100
        page     = 0
        
        for page in range(1, 11):
            resp = self.search(q + "&per_page=" + str(per_page) + 
                               "&page=" + str(page))
            
            # Check if the response was empty, so that we can reduce
            # the load on the GitHub API servers.
            if not resp["items"]:
                break
    
    def search(self, q="language:PHP", sort=None, order=None):
        """
        Search GitHub for 'q'.
        Any search is limited to 1000 results.
        """
        # Could yield problems, because no deep copy is done.
        # TODO: (maybe)
        resp = r.get(self.addOAuth(self.LINK_SEARCH_API + "?q=" + q),
                     headers=self.HEADERS)
        
        decoded = json.loads(resp.text)
        
        for _dict in decoded["items"]: 
            print _dict["clone_url"]
            
        return decoded
    
    def showRateLimit(self):
        resp = r.get(self.addOAuth(self.LINK_RATE_LIMIT))
            
        _dict = json.loads(resp.text)["resources"]
        
        print "Rate Limits:"
        print "core:"  , _dict["core"]
        print "search:", _dict["search"]
    
    def addOAuth(self, url):
        """
        Add the OAuth get-parameter to the specified 'url'.
        """
        token_query = "access_token=" + self.OAUTH["token"]
        if url.find('?') != -1:
            url += "&" + token_query
        else:
            url += "?" + token_query 
    
        return url