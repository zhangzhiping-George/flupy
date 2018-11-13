import os
import json
import warnings

from urllib.request import urlopen

url = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'downloads/osconfeed.json'


def load():
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(url, JSON)
        warnings.warn(msg)
        with urlopen(url) as remote, open(JSON, 'wb') as local:
            local.write(remote.read())

    with open(JSON) as fp:
        return json.load(fp)
