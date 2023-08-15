import os
import binascii


def generate_key():
    """
        Generate a random hex key for the application
    """
    return '0x' + binascii.hexlify(os.urandom(6)).decode()
