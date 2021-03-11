import argparse
import json
import models
import pymongo
from flask import Flask, abort, request, jsonify
import spider

app = Flask(__name__)


@app.route('/api/', methods=['POST'])
def post_app_id():
    if not request.json or 'id' not in request.json:
        abort(400)
    appid = {
        'id': request.json['id']
    }
    return models.JSONEncoder().encode(connect_database('mongodb://127.0.0.1:27017', str(appid["id"])))


@app.route('/')
def home():
    abort(400)


def connect_database(mongo_url, appid):
    client = pymongo.MongoClient(mongo_url)
    db = client["game_data"]
    col = db[appid]
    collist = db.list_collection_names()
    if appid in collist:  # 判断 sites 集合是否存在
        return_list = list()
        for x in col.find():
            return_list.append(x)
        return return_list
    else:
        spider.put_gameinfo_to_db('http://steamdb.info/app/' + appid + '/?cc=cn', mongo_url)
        return_list = list()
        for x in col.find():
            return_list.append(x)
        return return_list


# if __name__ == "__main__":
#     app.run(debug=True, port=8080)
#     connect_database('mongodb://127.0.0.1:27017', '578080')
#     print(models.JSONEncoder().encode(connect_database('mongodb://127.0.0.1:27017', '578080')))
#     print(connect_database('mongodb://127.0.0.1:27017', '578080'))
