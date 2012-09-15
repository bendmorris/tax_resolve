import os
import cPickle as pickle


home_dir = os.path.expanduser('~')
DATA_DIR = os.path.join(home_dir, '.tax_resolve')
if not os.path.exists(DATA_DIR):
    try:
        os.mkdir(DATA_DIR)
    except: DATA_DIR = os.getcwd()

cache_path = lambda name: os.path.join(DATA_DIR, '%s.cache' % name)

def get_cache(name):
    return pickle.load(open(cache_path(name), 'r'))
    
def save_cache(obj, name):
    pickle.dump(obj, open(cache_path(name), 'w'), protocol=-1)
