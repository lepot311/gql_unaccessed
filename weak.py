import json
import logging
import weakref

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


class AccessedNamespace:
    def __init__(self, data):
        self._data = data

        self._accessed = self._build_dict(data)

    def _build_dict(self, data, value=None):
        '''
        Walk through a dict and build up a copy.
        If the value is a dict, recurse,
        otherwise, set the value to False.
        '''
        result = {}
        for k, v in data.items():
            if type(v) is dict:
                result[k] = self._build_dict(v)
            else:
                result[k] = False
        return result

    def __getattr__(self, name):
        '''
        Update this attr's value in self._accessed and return the original attr.
        '''
        LOGGER.debug("__getattr__ %s", name)

        if name not in ('_data', '_accessed'):
            if type(self._accessed[name]) is not dict:
                LOGGER.debug("[ACCESSED] %s", name)
                # update the accessed dict to show this has been accessed
                self._accessed[name] = True
            # return the value from the self._data object
            return object.__getattribute__(self, '_data')[name]
        return object.__getattribute__(self, name)


def make_request():
    # example of what we might get back from gql client
    data = {
        'a': 1,
        'b': 2,
        'customer': {
            'name' : 'Erik',
            'email': 'erik@example.com',
        },
    }
    # build a chain of AccessedNamespace objects
    # object_hook replaces each JSON object (dict) with an AccessedNamespace
    response = json.loads(
        json.dumps(data),
        object_hook=lambda d: AccessedNamespace(d)
    )
    return response
