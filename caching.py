import os
import cPickle as pickle

try: DATA_DIR = os.path.dirname(os.path.realpath(__file__))
except: DATA_DIR = os.getcwd()


cache_path = lambda name: os.path.join(DATA_DIR, '%s.cache' % name)

def get_cache(name):
    return pickle.load(open(cache_path(name), 'r'))
    
def save_cache(obj, name):
    pickle.dump(obj, open(cache_path(name), 'w'), protocol=-1)
