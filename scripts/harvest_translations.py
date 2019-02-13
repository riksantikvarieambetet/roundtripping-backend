import sys
import json

import requests

from pywikibot.pagegenerators import CategorizedPageGenerator
from pywikibot import Site, Category

try:
    arg = sys.argv[1]
except IndexError:
    print('no given category')
    exit()

collections = False
with open('roundtripping/static/collections.json') as json_file:
    collections = json.load(json_file)

found_collection = False
for c in collections:
    if c['generator_value'] == arg:
        found_collection = c['id']
        break

if not found_collection:
    print('Could not find a colletion for the given category')

site = Site('commons', 'commons')
cat =  Category(site, 'Category:{}'.format(arg))
gen = CategorizedPageGenerator(cat, recurse=False, namespaces=6)
endpoint = 'https://commons.wikimedia.org/w/api.php?format=json&action=wbgetentities&ids='

final_translations = list()

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

for page in gen:

    media_id = 'M{}'.format(page.pageid)
    translations = False
    local_id = 'in-the-future'

    print(media_id)
    url = endpoint + str(media_id)
    response = requests.get(url)
    data = response.json()
    try:
        labels = data['entities'][list(data['entities'].keys())[0]]['labels'].values()
    except KeyError:
        continue

    translations = list(labels)

    final_obj = {}
    final_obj['mediainfo_id'] = media_id
    final_obj['local_id'] = local_id
    final_obj['translations'] = translations
    final_translations.append(final_obj)

for i, chunk in enumerate(chunks(final_translations, 50)):
    page = i + 1

    with open('src/static/cache/translations/{}_{}.json'.format(found_collection, page), 'w') as outfile:
        json.dump(chunk, outfile)
