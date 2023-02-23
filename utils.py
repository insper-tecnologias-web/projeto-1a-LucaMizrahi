from pathlib import Path
import json
from database import Database

CUR_DIR = Path(__file__).parent

def extract_route(request):
    if request == '':
        return ''
    retorno = request.split(' ')[1]
    retorno = retorno[1:]
    print(retorno)
    return retorno

request = "GET /img/logo-getit.png HTTP/1.1"
extract_route(request)


def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

'''def read_file(path):
    full_path = CUR_DIR / path
    with open(full_path, 'rb') as f:
        return f.read()'''

def load_data():
    db = Database('banco')
    notes = db.get_all()
    return notes

def load_template(filename):
    FULL_PATH = CUR_DIR / 'templates' / filename
    with open(FULL_PATH, 'r', encoding='UTF-8') as f:
        loaded = f.read()
    return loaded

def add_json(params):
    FULL_PATH = CUR_DIR / 'data' / 'notes.json'
    with open(FULL_PATH, 'r', encoding='UTF-8') as f:
        loaded = json.load(f)
    loaded.append(params)
    with open(FULL_PATH, 'w', encoding='UTF-8') as f:
        f.write(json.dumps(loaded))

def build_response(body='', code=200, reason='OK', headers=''):
    if headers == '':
        return f'HTTP/1.1 {code} {reason}\n\n{body}'.encode()
    else:
        return f'HTTP/1.1 {code} {reason}\n{headers}\n\n{body}'.encode()

