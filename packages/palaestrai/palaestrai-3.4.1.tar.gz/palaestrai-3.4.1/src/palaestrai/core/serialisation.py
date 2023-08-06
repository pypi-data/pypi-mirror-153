import pickle
import zlib


def serialize(request):
    pick = pickle.dumps(request)
    return zlib.compress(pick)


def deserialize(response):
    if response is not None:
        decompress = zlib.decompress(response[0])
        return pickle.loads(decompress)
    else:
        return None
