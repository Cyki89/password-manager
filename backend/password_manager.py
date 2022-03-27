import os
import string
import random
import clipboard
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from .exceptions import IntegrityError


def generate_salt():
    return base64.b64encode(os.urandom(16)).decode('utf-8')


def generate_secret_key(password_provided, salt_provided):
    password = password_provided.encode()  
    salt = salt_provided.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt_password(password_provided, key):
    passowrd = password_provided.encode()
    fernet = Fernet(key)
    
    encrypted = fernet.encrypt(passowrd)
    return encrypted.decode()
    

def decrypt_password(password_provided, key):
    passowrd = password_provided.encode()
    fernet = Fernet(key)

    try:
        decrypted = fernet.decrypt(passowrd)
        return decrypted.decode()
    except InvalidToken:
        raise IntegrityError("Invalid Master Password")


def valid_secret_key(secret_key, veryfication_password):
    try:
        decrypt_password(key=secret_key, password_provided=veryfication_password)
        return True
    except IntegrityError:
        return False


def generate_password(**options):
    length = max(options.pop('length'), 8)
    
    is_characterset = sum(option for option in options.values()) > 0
    if not is_characterset:
        raise ValueError(f"Password should contain at least 1 characterset")

    lower = string.ascii_lowercase if options['contain_lower'] else ''
    upper = string.ascii_uppercase if options['contain_upper'] else ''
    num = string.digits if options['contain_digits'] else ''
    symbols = string.punctuation if options['contain_symbols'] else ''

    charsets = [lower, upper, num, symbols]

    selected = [random.choice(charset) for charset in charsets if charset]

    while len(selected) < length:
        idx = random.randrange(0, len(charsets))
        if charsets[idx]:
            selected.append(random.choice(charsets[idx]))
    
    random.shuffle(selected)

    return ''.join(selected)


def copy_to_clipboard(txt):
    clipboard.copy(txt)

