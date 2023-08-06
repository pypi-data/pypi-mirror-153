import hashlib
import random
from .user import User

def gen_sha1(user: User,version: int) -> str:
    random.seed(a=user.gen_seed_value(),version=version)
    order = [random.randint(0,5) for i in range(0,6)]
    attrs = user.as_attr_list()
    hash_str = ""
    for o in order:
        hash_str += attrs[o]
    return hashlib.sha1(bytes(hash_str,'utf-8')).hexdigest()