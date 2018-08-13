import os
import tempfile
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--key")
parser.add_argument("--value")
args = parser.parse_args()

key = args.key
value = args.value

if key is None:
    exit()

json_dict = {}
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

if os.path.isfile(storage_path):
    with open(storage_path, 'r') as f:
        text = f.read()
        json_dict = json.loads(text)

stored_values = json_dict.get(key, [])
stored_values = list(stored_values)

if value is not None:
    stored_values.append(value)
    json_dict[key] = stored_values

    with open(storage_path, 'w') as f:
        json.dump(json_dict, f)
else:
    print(", ".join(stored_values))
