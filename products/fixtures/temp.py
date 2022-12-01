import json

with open('categories.json', 'rb') as f, open('categories_01.json', 'w') as wr:
    red = json.load(f)
    json.dump(red, wr, indent=4)