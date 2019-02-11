from flask import current_app
from flask_restful import Resource

class Institutions(Resource):
    def get(self):
        return current_app.send_static_file('institutions.json')
