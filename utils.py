import json

def list_objects_from_json(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    objects = set()

    for hit in data.get("hits", {}).get("hits", []):
        deepstream_msgs = (
            hit.get('_source', {}).get('deepstream-msg', []) +
            hit.get('fields', {}).get('deepstream-msg', [])
        )
        for entry in deepstream_msgs:
            parts = entry.split("|")
            if len(parts) >= 6:
                objects.add(parts[5])

    return sorted(objects)
