""" converts yml to json"""
import json
import pathlib
import sys
import yaml

from qary import init

YAML_FILEPATH = pathlib.Path(init.DATA_DIR, 'testsets', 'dialog', 'qa-2020-04-25.yml')
JSON_FILEPATH = pathlib.Path(init.DATA_DIR, 'testsets', 'dialog', 'qa-2020-04-25.json')


def yaml_to_json(yamlpath=YAML_FILEPATH, jsonpath=JSON_FILEPATH):
    r"""converts yaml to json file

    >>> yamlpath = pathlib.Path(init.DATA_DIR, 'testsets', 'dialog', 'qa-2020-04-25.yml')
    >>> jsonpath = yamlpath.parent / (yamlpath.name[:-3] + 'json')
    >>> yaml_to_json(yamlpath=yamlpath, jsonpath=jsonpath)
    PosixPath('.../testsets/dialog/qa-2020-04-25.json')
    """

    with open(yamlpath) as yml:
        data = yaml.full_load(yml)

    with open(jsonpath, 'w') as js:
        json.dump(data, js, ensure_ascii=False, indent=2)

    return jsonpath


if __name__ == '__main__':
    yamlpath = YAML_FILEPATH
    jsonpath = JSON_FILEPATH
    if len(sys.argv) == 3:
        yamlpath = sys.argv[1]
        jsonpath = sys.argv[2]
    elif len(sys.argv) == 2:
        yamlpath = sys.argv[1]
        jsonpath = yamlpath + '.json'
    yaml_to_json(yamlpath=yamlpath, jsonpath=jsonpath)
