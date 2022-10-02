import json
import logging
import os
import time


def retry(function, attempts=10, fallback=None):
    error = None
    for _ in range(attempts):
        try:
            return function()
        except Exception as e:
            time.sleep(0.1)
            error = e

    if fallback:
        return fallback
    raise error


def path(file=None):
    return os.path.dirname(os.path.realpath(file or __file__))


def data_path():
    directory = os.path.dirname(os.path.realpath(__file__))
    while not directory.endswith('app'):
        directory = directory[:-1]
    
    directory += '\\data'

    return directory

def assert_extension(filename, required_extension):
    _, extension = os.path.splitext(filename)
    assert extension == required_extension, f'file {filename} must end in {required_extension}'


read_json_cache = {}


def read_json(file, fallback=None, cache_timeout=None, mpath=None):
    assert_extension(file, '.json')

    if cache_timeout and file in read_json_cache:
        cache, timestamp = read_json_cache[file]
        age = time.time() - timestamp
        if age < cache_timeout:
            return cache
    
    p = mpath or data_path()

    if os.path.exists(f'{p}/{file}'):
        def read():
            with open(f'{p}/{file}', 'r') as s:
                result = json.load(s)
                read_json_cache[file] = result, time.time()
                return result
        return retry(read, fallback=fallback)

    with open(f'{p}/{file}', 'w') as s:
        mdict = fallback if fallback is not None else {}
        json.dump(mdict, s, indent=4)
        return mdict

def read_txt(file, fallback=None, mpath=None):
    assert_extension(file, '.txt')

    p = mpath or data_path()

    if os.path.exists(f'{p}/{file}'):
        with open(f'{p}/{file}', 'r') as f:
            return f.read()

    with open(f'{p}/{file}', 'w') as f:
        string = fallback or ''
        f.write(string)
        return string

def write_txt(file, text, mpath=None):
    assert_extension(file, '.txt')

    logging.debug(f'writing {text} to {file}' if len(text) < 20 else f'writing to {file}')

    with open(f'{mpath or data_path()}/{file}', 'w') as f:
        f.write(text)

def write_json(file, mdict, mpath=None):
    assert_extension(file, '.json')

    logging.debug(f'writing {mdict} to {file}' if len(
        str(mdict)) < 20 else f'writing to {file}')

    with open(f'{mpath or data_path()}/{file}', 'w') as s:
        json.dump(mdict, s, indent=4)

def env_is_true(name: str, default=True) -> bool:
    default_str = 'True' if default else 'False'
    env_variable = os.environ.get(name, default=default_str).lower()
    return env_variable in ('true', 't', '1')

def get_nested_value(json, *keys):
    if keys[0] not in json: return None
    if len(keys) == 1: return json[keys[0]]
    return get_nested_value(json[keys[0]], *keys[1:])
