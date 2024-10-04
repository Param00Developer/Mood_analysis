import json

from bson import ObjectId

class ObjectIdEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super().default(obj)

def write_dict_to_json(data, filename):
    # Write the list of dictionaries to a JSON file
    with open(filename, 'a') as json_file:
        for  item in data:
            json.dump(item, json_file, cls=ObjectIdEncoder, indent=4) 
            json_file.write(",\n")

def start_json_file(filename):
    # Open the file and write the opening bracket
    with open(filename, 'w') as json_file:
        json_file.write("[\n")  

def end_json_file(filename):
    # Open the file in read/write mode
    with open(filename, 'rb+') as json_file:
        json_file.seek(0, 2)  
        pos = json_file.tell()      
        # Traverse back to remove the last comma
        while pos > 0:
            pos -= 1
            json_file.seek(pos)  # Move the cursor back by one byte
            if json_file.read(1) == b',':
                json_file.seek(pos)  
                break
        json_file.truncate()  
        json_file.write(b"\n]")  # Add the closing bracket
