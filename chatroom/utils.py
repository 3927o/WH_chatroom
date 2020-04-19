import requests
import hashlib


def generate_avatar(name, path):
    name_hash = hashlib.md5(name.encode('utf-8')).hexdigest()
    url = 'https://cdn.v2ex.com/gravatar/{}?s=100&r=g&d=identicon'.format(name_hash)
    resp = requests.get(url)

    f = open(path, 'wb')
    f.write(resp.content)
    f.close()
