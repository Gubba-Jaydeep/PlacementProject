from django.db import models

# Create your models here.

import pymongo
import datetime
import bson

# Create your models here.

class Forum:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://jd254:pass123@cluster0-shard-00-00-yftzb.mongodb.net:27017,cluster0-shard-00-01-yftzb.mongodb.net:27017,cluster0-shard-00-02-yftzb.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
        self.mydb = self.client["Forum"]

    def getQuestions(self):
        mycol = self.mydb["question"]
        res = []
        for x in mycol.find({},{"answers":0}):
            #x['question']=x['question'][:min(50,len(x['question']))]
            res.append(x)
        return res

    def getQuestion(self,qID):
        mycol=self.mydb["question"]
        return mycol.find_one({'qID':qID})

    def getAnswers(self,qID):
        mycol=self.mydb["question"]
        x=mycol.find_one({"qID":int(qID)})
        #x['answers']
        return x

    def addQuestion(self,q):
        mycol = self.mydb["question"]
        if mycol.find_one({"question": q['question']}) == None:
            q['date']=datetime.datetime.now()
            qID=mycol.insert_one(q)
            count=0
            for i in mycol.find():
                count+=1
            mycol.update_one({"_id":qID.inserted_id},{"$set":{'qID':count+1}})
        else:
            qID=None
            return False
        qID=qID.inserted_id
        uID=q['uID']
        mycol = self.mydb["users"]
        x = mycol.find_one({"uID": uID})
        x['qAsked'].append(qID)
        mycol.update_one({"uID": uID}, {"$set": x})
        return True

    def addAnswer(self,qID,answer):

        answer['date'] = datetime.datetime.now()
        mycol = self.mydb["question"]
        x=mycol.find_one({"qID":qID})
        x['answers'].append(answer)
        mycol.update_one({"_id":qID},{"$set":x})
        return True

    def getUsers(self):
        pass

    def addUser(self,user):
        mycol = self.mydb["users"]
        mycol.insert_one(user)

    def getUser(self,uID):
        mycol = self.mydb["users"]
        return mycol.find_one({'uID':uID})








