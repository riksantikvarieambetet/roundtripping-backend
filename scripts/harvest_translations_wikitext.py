import datetime
import sys
import json

import requests
import mwparserfromhell

from pywikibot.pagegenerators import CategorizedPageGenerator
from pywikibot import Site, Category

try:
    arg = sys.argv[1]
except IndexError:
    print('no given category')
    exit()

collections = False
with open('src/static/collections.json') as json_file:
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

final_translations = list()

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

n_sv_translations = 0
n_en_translations = 0
for page in gen:
    wikicode = mwparserfromhell.parse(page.text)

    template_to_parse = False
    for template in wikicode.filter_templates():
        if template.name.matches('Musikverket-image'):
            template_to_parse = template

    if not template_to_parse:
        print('failed to find given template')
        continue

    media_id = 'M{}'.format(page.pageid)
    local_id = mwparserfromhell.parse(template_to_parse).filter_templates()[0].get('ID').value.lstrip()

    translations = list()
    for description in mwparserfromhell.parse(template_to_parse).filter_templates()[0].get('description').value.filter_templates():
        translation = {}
        # prep stats and ignore everything that's not English or Swedish
        if str(description.name) == 'sv':
            n_sv_translations += 1
        elif str(description.name) == 'en':
            n_en_translations += 1
        else:
            continue

        translation['language'] = str(description.name)
        translation['value'] = str(description.get(1))
        translations.append(translation)

    final_obj = {}
    final_obj['mediainfo_id'] = media_id
    final_obj['local_id'] = str(local_id)
    final_obj['translations'] = translations
    final_translations.append(final_obj)

t = datetime.datetime.now()
stats = {}
stats['progress'] = round(100 * n_en_translations / n_sv_translations)
stats['timestamp'] = t.strftime('%Y-%m-%d-%H-%M')
with open('src/static/cache/translations/{}_stats.json'.format(found_collection), 'w') as outfile:
    json.dump(stats, outfile)

for i, chunk in enumerate(chunks(final_translations, 50)):
    page = i + 1

    with open('src/static/cache/translations/{}_{}.json'.format(found_collection, page), 'w') as outfile:
        json.dump(chunk, outfile)