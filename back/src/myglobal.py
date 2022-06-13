import json
from src.db import DbManager

config = json.load(open('config.json','r',encoding="utf-8"))
dbmanager = DbManager(config["mysql"])