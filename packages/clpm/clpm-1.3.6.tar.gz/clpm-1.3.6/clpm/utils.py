# PROJECT: CLPM -- Command Line Password Manager
# AUTHOR: alexjaniak
# FILE: General helper functions.


# IMPORTS
from clpm.sql_utils import *
import prettytable
import os
from pathlib import Path
import click 
from Crypto.Hash import SHA3_256
from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes

def print_table(cursor, password):
    """Print a table from cursor."""
    rows = cursor.fetchall() # Get all rows from the cursor. 
    table = prettytable.PrettyTable()
    table.field_names = ["id", "accounts", "username", "password", "email", "tag"]
    for row in rows:
        row = list(row) # Split into a list of elements.
        key, salt = get_private_key(password, salt=row[7]) # Get key hash
        row[3] = decode_aes_256(row[3], key, row[6])
        table.add_row(row[:6])
    click.echo(table.get_string())

def is_blank(string):
    """Checks if string is either empty or just whitespace."""
    if not string or string.isspace():
        return True
    return False

def prompt_field(prompt):
    """Prompts user for a for a field."""
    field = click.prompt(prompt, default="",show_default=False)
    if is_blank(field): field = None
    return field

def prompt_rfield(prompt, prompt_name):
    """Prompts user for a required field."""
    while True:
        field = click.prompt(prompt, default="", show_default=False)
        if not is_blank(field): return field
        click.echo("Field {} is required.".format(prompt_name))
    
def qprompt(string):
    """Quit option for prompt."""
    if not string == None and string.strip() == "q":
        click.echo("Aborted!")
        return True
    return False

def digest_sha_256(string):
    """Hashes string and returns hexdigest using SHA-256."""
    bstring = string.encode() # Convert to bytes.
    sha_256 = SHA3_256.new() # SHA_256 encoder.
    sha_256.update(bstring) # Encode string.
    return sha_256.hexdigest() # Return hexdigest.

def get_private_key(password, salt = None):
    """Creates key from password."""
    if salt == None: salt = get_random_bytes(32)
    encoded = password.encode('UTF-8') # Encode into bytes. 
    key = KDF.scrypt(encoded, salt, 32, N=2**14, r=8, p=1) 
    return key, salt

def encode_aes_256(text, key):
    """Encodes a string using AES-256."""
    cipher = AES.new(key, AES.MODE_CBC)
    ct_b = cipher.encrypt(pad(text.encode('UTF-8'), AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_b).decode('utf-8')
    return ct, iv

def decode_aes_256(ciphertext, key, iv):
    """Decodes a AES-256 encoded string."""
    try:
        iv = b64decode(iv)
        ct = b64decode(ciphertext)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        text = unpad(cipher.decrypt(ct), AES.block_size)
        return text.decode('UTF-8')
    except (ValueError, KeyError) as e:
        print("Incorrect decryption")
        raise 

def encrypt_password(password, acc_password):
    """Encodes a string (acc_password) using the key generated from (password)."""
    key, salt = get_private_key(password)
    ct, iv = encode_aes_256(acc_password, key)
    return ct, iv, salt

    