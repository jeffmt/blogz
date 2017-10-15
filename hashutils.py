import hashlib

def make_pw_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def password_matches_hash(password, pw_hash):
    if make_pw_hash(password) == pw_hash:
        return True
    return False
