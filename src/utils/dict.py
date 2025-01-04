from itertools import chain

def dict_union(*args):
    return dict(chain.from_iterable(d.items() for d in args))
