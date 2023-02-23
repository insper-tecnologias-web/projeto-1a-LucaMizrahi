import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

class Database:
    def __init__(self, name):
        self.conn = sqlite3.connect(name+'.db')
        
        self.conn.execute("""CREATE TABLE IF NOT EXISTS note ( id INTEGER PRIMARY KEY,
                                            title TEXT,
                                            content TEXT NOT NULL);""")
    
    def add(self, note):
        command = f'INSERT INTO note (title, content) VALUES ("{note.title}", "{note.content}");'
        self.conn.execute(command)
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute('SELECT id, title, content FROM note;')
        notes = []
        for linha in cursor:
            note = Note()
            note.id = linha[0]
            note.title = linha[1]
            note.content = linha[2]
            notes.append(note)
        return notes
    
    def update(self, entry):
        command = f'UPDATE note SET title="{entry.title}", content="{entry.content}" WHERE id={entry.id};'
        self.conn.execute(command)
        self.conn.commit()
    
    def delete(self, note_id):
        command = f'DELETE FROM note WHERE id={note_id};'
        self.conn.execute(command)
        self.conn.commit()

