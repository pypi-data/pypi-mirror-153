import os
import json


def main():
    for subdir, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.json'):
                path = os.path.join(subdir, file)
                with open(path, 'r') as f:
                    try:
                        content = json.load(f)
                    except:
                        continue
                with open(path, 'w') as f:
                    f.write(json.dumps(content, indent=4))
