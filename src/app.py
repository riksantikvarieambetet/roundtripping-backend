import sys

from flask import Flask
from flask_restful import Api

from views.institutions import Institutions
from views.collections import Collections
from views.collection import Collection
from views.changes.translations import Translations
from views.changes.translations_progress import Translations_Progress

# http://www.ianbicking.org/illusive-setdefaultencoding.html
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding('utf-8')

app = Flask(__name__)
api = Api(app)

# CORS headers
@app.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
    return resp

# routes
api.add_resource(Institutions, '/institutions')
api.add_resource(Collections, '/institutions/<uuid:institution>/collections')
api.add_resource(Collection, '/institutions/<uuid:institution>/collections/<uuid:collection>')
api.add_resource(Translations, '/changes/<uuid:collection>/translations')
api.add_resource(Translations_Progress, '/changes/<uuid:collection>/translations/progress')

if __name__ == '__main__':
    app.run()
