import os
import sys
try: DATA_DIR = os.path.dirname(os.path.realpath(__file__))
except: DATA_DIR = os.getcwd()
import urllib
import urllib2
import re
from pyquery import PyQuery as p
import cPickle as pickle


try: tnrs_cache = pickle.load(open(os.path.join(DATA_DIR, 'tnrs.cache'), 'r'))
except: tnrs_cache = {}


URL = "http://tnrs.iplantc.org/tnrsm-svc/matchNames?retrieve=best&names=%s"

def tnrs_lookup(name, TIMEOUT=10, CACHE=True):
    '''
    Look up "name" on the TNRS web service. If a most likely standard name can be identified, 
    returns that name. Returns False if no or ambiguous result.
    '''

    name = name.replace("'", '').lower()
    if name in tnrs_cache and CACHE:
        return tnrs_cache[name]

    # lookup canonical plant names on TNRS web service
    true, false, null = True, False, None
    try:
        response = urllib2.urlopen(URL % name.replace(' ', '%20'), timeout=TIMEOUT).read()

        response_dict = eval(response)
        sci_name = response_dict['items'][0]['nameScientific']

        if sci_name: result = sci_name
        else: result = None

    except Exception as e:
        print e
        result = False

    # cache results and return
    tnrs_cache[name] = result
    if CACHE: pickle.dump(tnrs_cache, open(os.path.join(DATA_DIR, 'tnrs.cache'), 'w'), protocol=-1)
    return result
    

if __name__=='__main__':
    if len(sys.argv) > 1: names = sys.argv[1:]
    else: names = [raw_input('species name: ')]
    for name in names:
        print name, '->', tnrs_lookup(name)
