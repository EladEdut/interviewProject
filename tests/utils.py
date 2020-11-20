import random


def hash_collection(col):
    return hash(frozenset(hash_dict(dict(dct)) for dct in col))


def hash_dict(dct):
    return hash(frozenset(dct.items()))


def get_random_name(name):
    bot_id = int(1000000 * random.random())
    return f"{name}-{bot_id}"
