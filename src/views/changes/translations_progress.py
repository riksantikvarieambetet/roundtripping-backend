import json

from pathlib import Path

from flask import current_app, request
from flask_restful import Resource, abort

class Translations_Progress(Resource):
    def get(self, collection):
        data = False
        with open('static/collections.json') as json_file:
            data = json.load(json_file)

        found_collection = False
        for c in data:
            if c['id'] == str(collection):
                found_collection = c
                break

        if not found_collection:
            return abort(404, message='Could not find the collection')

        cache_path = Path('static/cache/translations/{}_stats.json'.format(collection))

        if cache_path.is_file():
            return current_app.send_static_file('cache/translations/{}_stats.json'.format(collection))
        return abort(404, message='Could not find progress file in translations cache(collection: {})'.format(collection))
