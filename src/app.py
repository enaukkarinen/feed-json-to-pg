import ijson

# Define a generator function to iterate through a large JSON file
def iterate_large_json(file_path):
    with open(file_path, 'r') as f:
        objects = ijson.items(f, 'entities.item')  # 'item' is used here for each object in the array
        for obj in objects:
            yield obj

file_path = './input/title-boundary.json'


print("running...")

for idx, item in enumerate(iterate_large_json(file_path)):
    print(f"Processing item {idx}: {item}")
    if idx == 9:  # Stop after the first 10 items (optional)
        break
