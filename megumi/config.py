import toml
from typing import Optional
import uuid
from catconfig import CatConfig

default_config = {
    'api': {
        'host': '127.0.0.1',
        'port': 8091,
        'auth_token': None
    },
    'runtime': {
        'data_path': 'runtime'
    },
    'downloader': {
        'type': 'aria2',
        'aria2': {
            'address': 'http://localhost:6800',
            'secret': None
        }
    },
    'logging': {
        'no_ansi': False,
        'level': 'INFO'
    }
}

config = CatConfig(data=default_config)