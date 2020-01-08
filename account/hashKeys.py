import hashlib
import hmac
from urllib.parse import urlencode

from account import keys as k

privateKey = k.secretKey()


def hashIt(params):
    par = []

    for i in params:
        query_string = urlencode(i)
        par.append(hmac.new(privateKey.encode('utf-8'),
                            query_string.encode('utf-8'), hashlib.sha256).hexdigest())

    return par
