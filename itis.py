import os
import sys
try: DATA_DIR = os.path.dirname(os.path.realpath(__file__))
except: DATA_DIR = os.getcwd()
import urllib
import urllib2
import re
from pyquery import PyQuery as p
import cPickle as pickle


try: itis_cache = pickle.load(open(os.path.join(DATA_DIR, 'itis.cache'), 'r'))
except: itis_cache = {}


def itis_lookup(name, TIMEOUT=10, CACHE=True):
    '''
    Look up "name" on itis.gov. If a standard name can be identified, returns
    that name. Returns False if no or ambiguous result.

    If a name matches multiple species that are all members of the same genus,
    itis_lookup will return "Genus sp1/sp2/sp3..."
    '''

    name = name.replace("'", '').lower()
    if name in itis_cache and CACHE:
        return itis_cache[name]

    url = 'http://www.itis.gov/servlet/SingleRpt/SingleRpt'
    values = {'search_topic': 'all', 
              'search_kingdom':'every', 
              'search_span':'containing', 
              'search_value': name.decode(), 
              'categories':'All', 
              'source':'html', 
              'search_credRating': 'All'}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req, timeout=TIMEOUT)
    html = response.read()

    # parse results to pull out unique species
    results = [s.tail for s in p(html)('td.body a')]
    results = sum([re.findall('Species: [A-Z][a-z ]*', result) for result in results], [])
    results = [s.split(':')[1].strip() for s in results]
    
    if results:
        genus = set()
        all_species = []
        for this_species in results:
            genus.add(this_species.split()[0])
            if len(genus) > 1: return False
            all_species.append(' '.join(this_species.split()[1:]))
        species = list(genus)[0] + ' ' + '/'.join(sorted(list(set(all_species))))
        itis_cache[name] = species
    else:
        itis_cache[name] = False

    if CACHE: pickle.dump(itis_cache, open(os.path.join(DATA_DIR, 'itis.cache'), 'w'), protocol=-1)

    return itis_cache[name]


if __name__=='__main__':
    if len(sys.argv) > 1: names = sys.argv[1:]
    else: names = [raw_input('species name: ')]
    for name in names:
        print name, '->', itis_lookup(name)
