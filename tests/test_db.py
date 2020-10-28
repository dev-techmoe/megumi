from megumi import db
import os

def test_db_init(tmp_path):
    db.get_db(str(tmp_path) + '/db')
