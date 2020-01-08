def secretKey():
    return checkPublicKey("Your secret api key goes here")


def publicKey():
    return checkPrivateKey("Your public api key goes here")


def checkPrivateKey(key):
    if len(key) != 64:
        raise TypeError(key, "is no valid Binance private api key")
    else:
        return key


def checkPublicKey(key):
    if len(key) != 64:
        raise TypeError(key, "is no valid Binance public api key")
    else:
        return key
