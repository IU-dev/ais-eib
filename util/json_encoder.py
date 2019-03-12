from flask.json import JSONEncoder as FlaskJSONEncoder


class JSONEncoder(FlaskJSONEncoder):

    def default(self, o):
        if hasattr(o, "to_json"):
            return o.to_json()
        return super(JSONEncoder, self).default(o)
