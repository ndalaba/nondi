# String helper

import secrets

def generate_uuid(length):
    return secrets.token_hex(length)