import gluon.contrib.simplejson as simplejson
import types
import sys


class JSONRPCServiceBase:

    def __init__(self):
        self.methods = {}

    def response(self, id, result):
        return simplejson.dumps({'version': '1.1', 'id': id,
                                 'result': result, 'error': None})

    def error(self, id, code, message):
        return simplejson.dumps({
            'id': id,
            'version': '1.1',
            'error': {'name': 'JSONRPCError',
                      'code': code,
                      'message': message}
        })

    def add_method(self, name, method):
        self.methods[name] = method

    def process(self, data):
        data = simplejson.loads(data)
        id, method, params = data["id"], data["method"], data["params"]
        if method in self.methods:
            try:
                result = self.methods[method](*params)
                return self.response(id, result)
            except BaseException:
                etype, eval, etb = sys.exc_info()
                return self.error(id, 100, '%s: %s' % (etype.__name__, eval))
            except Exception:
                etype, eval, etb = sys.exc_info()
                return self.error(id, 100, 'Exception %s: %s' % (etype, eval))
        else:
            return self.error(id, 100, 'method "%s" does not exist' % method)

    def listmethods(self):
        return self.methods.keys()
