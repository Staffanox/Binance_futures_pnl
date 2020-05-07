import os
os.chdir("account")


def public_key():
    return check_public_key(read_file().get("PublicKey:"))


def secret_key():
    return check_private_key(read_file().get("SecretKey:"))


def check_private_key(key):
    if len(key) != 64:
        raise TypeError(key, "is no valid Binance private API-key")
    else:
        return key


def check_public_key(key):
    if len(key) != 64:
        raise TypeError(key, "is no valid Binance public API-key")
    else:
        return key


def read_file():
    keys = {}
    with open("keys") as file:
        for line in file:
            (key, val) = line.split()
            keys[key] = val
    return keys
