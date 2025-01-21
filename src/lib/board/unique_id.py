from binascii import hexlify
from machine import unique_id

def get_unique_id(): 
    return str(hexlify(unique_id()).decode('utf-8'))
