import pickle

def _load_pickled(path):
    return pickle.load(open(path, 'rb'))