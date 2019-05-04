from django.db import models

# Create your models here.

import pymongo

# Create your models here.

class Forum:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://jd254:pass123@cluster0-shard-00-00-yftzb.mongodb.net:27017,cluster0-shard-00-01-yftzb.mongodb.net:27017,cluster0-shard-00-02-yftzb.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
        self.mydb = self.client["Forum"]

    def getQuestions(self):
        mycol = self.mydb["question"]
        res = []
        for x in mycol.find({},{"answers":0}):
            res.append(x)
        return res

    def getAnswers(self,id):
        mycol=self.mydb["question"]
        x=mycol.find_one({"_id":id})
        return x['answers']

    def addQuestion(self,q):
        mycol = self.mydb["question"]
        qID=mycol.insert_one(q)
        qID=qID.inserted_id
        uID=q['uID']
        mycol = self.mydb["users"]
        x = mycol.find_one({"uID": uID})
        x['qAsked'].append(qID)
        mycol.update_one({"_id": uID}, {"$set": x})
        return True

    def addAnswer(self,qID,answer):
        mycol = self.mydb["question"]
        x=mycol.find_one({"_id":qID})
        x['answers'].append(answer)
        mycol.update_one({"_id":qID},{"$set":x})
        return True





