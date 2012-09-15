import sys
import caching
import urllib
import urllib2
import re
from pyquery import PyQuery as p


try: cache = caching.get_cache('itis')
except: cache = {}


def itis_lookup(name, TIMEOUT=10, CACHE=True):
    '''
    Look up "name" on itis.gov. If a standard name can be identified, returns
    that name. Returns False if no or ambiguous result.

    If a name matches multiple species that are all members of the same genus,
    itis_lookup will return "Genus sp1/sp2/sp3..."
    '''

    name = name.replace("'", '').lower()
    if name in cache and CACHE:
        return cache[name]

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
        cache[name] = species
    else:
        cache[name] = False

    if CACHE: caching.save_cache(cache, 'itis')

    return cache[name]


if __name__=='__main__':
    if len(sys.argv) > 1: names = sys.argv[1:]
    else: names = [raw_input('species name: ')]
    for name in names:
        print name, '->', itis_lookup(name)
