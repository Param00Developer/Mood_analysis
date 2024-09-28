import json

from bson import ObjectId

class ObjectIdEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super().default(obj)

def write_dict_to_json(data, filename):
    # Write the list of dictionaries to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, cls=ObjectIdEncoder, indent=4) 