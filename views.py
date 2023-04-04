from utils import load_data, load_template, build_response
import urllib.parse
from utils import add_json
from database import Database, Note
from utils import extract_route

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        corpo = urllib.parse.unquote_plus(corpo, encoding='utf-8', errors='replace')
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = valor
        
        add_json(params)

        return build_response(code=303, reason='See Other', headers='Location: /')

    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados.title, details=dados.content, id=dados.id)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)
    body = load_template('index.html').format(notes=notes)

    return build_response(body=body)

def delete(id):
    db = Database('banco')
    db.delete(id)
    return build_response(code=303, reason='See Other', headers='Location: /')

def update(request):
    route = extract_route(request)
    id = route.split('/')[1]
    
    db = Database('banco')
    note = db.get(id)

    body = load_template('edit.html').format(id=note.id, title=note.title, details=note.content)
    
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        corpo = urllib.parse.unquote_plus(corpo, encoding='utf-8', errors='replace')
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = valor
        
        note.title = params['titulo']
        note.content = params['detalhes']
        db.update(note)

        return build_response(code=303, reason='See Other', headers='Location: /')
    
    return build_response(body=body)

def avaliacao(request):
    body = load_template('avaliacao.html')
    return build_response(body=body)