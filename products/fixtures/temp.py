import json

with open('categories.json', 'rb') as f, open('categories_01.json', 'w', encoding='utf-8') as wr:
    read = json.load(f)
    json.dump(read, wr, indent=4)

with open('products.json', 'rb') as f, open('products_01.json', 'w', encoding='utf-8') as wr:
    read = json.load(f)
    json.dump(read, wr, indent=4)