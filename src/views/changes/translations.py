import json

from pathlib import Path

from flask import current_app, request
from flask_restful import Resource, abort


class Translations(Resource):
    def get(self, collection):
        args = request.args

        data = False
        with open('src/static/collections.json') as json_file:
            data = json.load(json_file)

        found_collection = False
        for c in data:
            if c['id'] == str(collection):
                found_collection = c['id']
                break

        if not found_collection:
            return abort(404, message='Could not find the collection')

        page = '1'
        if 'page' in args:
            page = args['page']

        cache_path = Path('src/static/cache/translations/{}_{}.json'.format(found_collection, page))

        if cache_path.is_file():
            return current_app.send_static_file('cache/translations/{}_{}.json'.format(found_collection, page))
        return abort(404, message='Could not find the given page {} in translations cache'.format(page))
