import sys
import caching
import urllib
import urllib2
import re
import json
from pyquery import PyQuery as p


try: cache = caching.get_cache('tnrs')
except: cache = {}


def tnrs_lookup(name, TIMEOUT=10, CACHE=True):
    '''
    Look up "name" on the TNRS web service. If a most likely standard name can be identified, 
    returns that name. Returns False if no or ambiguous result.
    '''

    name = name.replace("'", '').lower()
    if name in cache and CACHE:
        return cache[name]
        
    url = "http://tnrs.iplantc.org/tnrsm-svc/matchNames?retrieve=best&names=%s"

    # lookup canonical plant names on TNRS web service
    try:
        response = urllib2.urlopen(url % name.replace(' ', '%20'), timeout=TIMEOUT).read()

        #response_dict = eval(response, {}, {'true':True, 'false':False, 'null':None})
        response_dict = json.loads(response)
        sci_name = response_dict['items'][0]['nameScientific']

        if sci_name: result = sci_name
        else: result = None

    except Exception as e:
        print e
        result = False

    # cache results and return
    cache[name] = result
    if CACHE: caching.save_cache(cache, 'tnrs')
    return result
    

if __name__=='__main__':
    if len(sys.argv) > 1: names = sys.argv[1:]
    else: names = [raw_input('species name: ')]
    for name in names:
        print name, '->', tnrs_lookup(name)
