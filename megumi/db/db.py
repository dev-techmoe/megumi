# Fuck Pylint 
# "from unqlite import UnQLite" get `No name 'UnQLite' in module 'unqlite'pylint(no-name-in-module)``
import unqlite

db: unqlite.UnQLite = None

def create_collection_if_not_exist(collection_name: str):
    db = get_db()
    coll = db.collection(collection_name)
    if not coll.exists():
        coll.create()

def get_db(db_path: str=None, mem_db=False) -> unqlite.UnQLite:
    global db
    if db == None:
        db = unqlite.UnQLite(db_path if not mem_db else ':mem:')

        create_collection_if_not_exist('jobs')
        create_collection_if_not_exist('task_history')

    return db

def clean_db():
    global db
    db = None
