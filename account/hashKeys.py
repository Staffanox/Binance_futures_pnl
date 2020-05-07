import hashlib
import hmac
from urllib.parse import urlencode

from account import keys as k

privateKey = k.secret_key()


def hashIt(params):
    query_string = urlencode(params)
    return hmac.new(privateKey.encode('utf-8'),
                    query_string.encode('utf-8'), hashlib.sha256).hexdigest()
