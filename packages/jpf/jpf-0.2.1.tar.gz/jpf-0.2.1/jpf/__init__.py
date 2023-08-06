import os
import json
import plac


@plac.opt('indent', "format files with that indent level", type=int)
@plac.opt('sort_keys', "decide whether jpf should sort the keys", type=bool)
def format(indent=4, sort_keys=False):
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
                    f.write(json.dumps(content, indent=indent, sort_keys=sort_keys))


def main():
    plac.call(format)
