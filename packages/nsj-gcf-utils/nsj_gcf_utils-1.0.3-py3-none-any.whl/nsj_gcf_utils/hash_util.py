from hashlib import sha256
from nsj_gcf_utils.json_util import json_dumps


def hash_webhook(url, payload, key):
    if isinstance(payload, dict):
        payload = json_dumps(payload)

    hash: str = url + payload + key # tipagem para ajudar o autocomplete de IDEs

    return sha256(hash.encode()).hexdigest()