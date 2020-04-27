import util
from flask import jsonify
from bson import ObjectId
from flask_pymongo import PyMongo
from datetime import datetime, timedelta

class pymongo:

    def __init__(self, app):
        self.db = PyMongo(app).db
        self.excludeId = dict(_id=False)
    
    def get_msg(self, topic):
        return jsonify(self.db.Messages.find_one({'topic': topic}, self.excludeId))

    def get_user(self, email, Id=None):
        if not Id:
            return self.db.Users.find_one({'email':email})
        else:
            return self.db.Users.find_one({'email':email, '_id': ObjectId(Id)})
    
    def insert_user(self, data):
        data['password'] = util.encrypt(data['password'])
        return str(self.db.Users.insert_one(data).inserted_id)
    
    def get_latest(self):
        return list(self.db.Latest.find({}, self.excludeId, limit=10).sort('Date', -1))

    def get_trending(self):
        return list(self.db.Trending.find({}, self.excludeId, limit=10).sort([('Date', -1), ('Rank', 1)]))
    
    def search_latest_category(self, category, page):
        return list(self.db.Latest.find({'Category': category}, self.excludeId, 
                                        skip=(page-1)*100, limit=10).sort('Date', -1))

    def search_latest_date(self, date):
        return list(self.db.Latest.find({'Date': {'$gte': date, '$lt': date + timedelta(days=1)}}))
    
    def search_trending_date(self, date):
        return list(self.db.Trending.find({'PostedDate': {'$gte': date, '$lt': date + timedelta(days=1)}}))
    
    def search_author(self, name):
        return list(self.db.Latest.find({'Author': {
                '$regex':name, 
                '$options':'i'}}, 
            self.excludeId).sort('Date', -1))