import urllib
import urllib.parse
import urllib.request
import json
import gzip
from io import BytesIO

service_url = 'https://babelfy.io/v1/disambiguate'
lang = 'EN'
key = '2e40ff40-ee1b-4a94-ba7e-66d30c616145'
key2 = 'd65a7170-9d89-4703-ae2f-31dc31bdd24c'


def get_bbn_ids(text):

    params = {
        'text': text,
        'lang': lang,
        'key': key2
    }

    url = service_url + '?' + urllib.parse.urlencode(params)
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib.request.urlopen(request)

    if response.info().get('Content-Encoding') == 'gzip':
        buf = BytesIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = json.loads(f.read())

        list_synset_id = []
        # retrieving data
        try:
            for result in data:
                # retrieving BabelSynset ID
                synsetId = result.get('babelSynsetID')
                list_synset_id.append(synsetId)
        # C'è un numero massimo di richieste giornaliere
        except AttributeError:
            print(data)
            return None
        return list_synset_id
