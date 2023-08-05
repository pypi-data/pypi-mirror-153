'''Provides 'AppJSONEncoder', 'CacheJSONEncoder' JSONEncoder implementations, instances'''

import datetime
import json

from bson import ObjectId


class AppJSONEncoder(json.JSONEncoder):
    '''JSONEncoder implementation that converts 'ObjectId', 'datetime' objects to str'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        if isinstance(o, datetime.datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return True

        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)


app_encoder = AppJSONEncoder()
