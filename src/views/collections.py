import json

from flask import current_app
from flask_restful import Resource, abort

class Collections(Resource):
    def get(self, institution):
        data = False
        with open('src/static/collections.json') as json_file:
            data = json.load(json_file)

        collections = list()
        for c in data:
            if c['owner'] == str(institution):
                collections.append(c)

        if not collections:
            return abort(404, message='Could not find any collections owned by '.format(str(institution)))
        return collections
