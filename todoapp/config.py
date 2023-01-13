# import json
# config = json.load(open('db_config.json'))


#Database connection
import pymongo

client= pymongo.MongoClient('localhost',27017)
db= client.user_login_system
