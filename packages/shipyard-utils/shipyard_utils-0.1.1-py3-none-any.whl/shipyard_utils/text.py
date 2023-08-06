import hashlib


def hash_text(text_var, hash_algorithm='sha256'):
    """
    Hash the provided text with a specified hash_algorithm.
    """
    if hash_algorithm == 'sha256':
        hashed_text = hashlib.sha256(text_var.encode('ascii')).hexdigest()
    if hash_algorithm == 'sha512':
        hashed_text = hashlib.sha512(text_var.encode('ascii')).hexdigest()
    if hash_algorithm == 'md5':
        hashed_text = hashlib.md5(text_var.encode('ascii')).hexdigest()
    return hashed_text
