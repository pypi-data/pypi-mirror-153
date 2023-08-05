import pickle


def load(*args, **kwargs):
    return pickle_load(*args, **kwargs)


def save(*args, **kwargs):
    return pickle_save(*args, **kwargs)


def pickle_load(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def pickle_save(o, path):
    with open(path, 'wb') as f:
        pickle.dump(o, f)
