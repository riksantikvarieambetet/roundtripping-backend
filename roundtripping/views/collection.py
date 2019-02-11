import json

from flask import current_app
from flask_restful import Resource, abort

class Collection(Resource):
    def get(self, institution, collection):
        data = False
        with open('roundtripping/static/collections.json') as json_file:
            data = json.load(json_file)

        found_collection = False
        for c in data:
            if c['owner'] == str(institution):
                if c['id'] == str(collection):
                    found_collection = c
                    break

        if not found_collection:
            return abort(404, message='Could not find the collection')
        
        return found_collection
