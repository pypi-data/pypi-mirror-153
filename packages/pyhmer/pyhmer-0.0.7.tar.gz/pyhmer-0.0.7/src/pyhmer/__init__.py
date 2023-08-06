import random
import pkg_resources

ANIMAL_RHYMES_PATH = ('animal_rhymes.csv')

def _stream(resource_name):
    stream = pkg_resources.resource_stream(__name__, resource_name)
    return stream

def get_list(stream):
    _list = []
    for row in stream:
        _list.append(row.decode('utf-8').strip())
    return _list

def get_animal_rhyme():
    stream = _stream(ANIMAL_RHYMES_PATH)
    rhyme_list = get_list(stream)
    return random.choice(rhyme_list)