from pymongo import MongoClient
import  os
import pandas as pd
from flask import send_from_directory


client = MongoClient("mongodb+srv://pyhackons:pyhackons@cluster0.ajjz3.mongodb.net/crowdengine?retryWrites=true&w=majority")
db = client['CrowdEngine']
doc = db['movies']
client.close()


movieslist = list(doc.find({'Movies': { '$exists': 'true' } },{'Movies':1,'_id':0})) #list(doc.find({'movie': { '$exists': 'true' } },{'movie':1,'_id':0}))

movieslist  = [i['Movies'] for i in movieslist]
movieslist = list( set( movieslist ) )
size = len(movieslist)


def page(pg , index):
    
    if pg == 'next':
        if size-1 > index:
            return movieslist[index+1]
        elif size-1 == index:
            return movieslist[0]
    elif pg == 'pre':
        if index == 0 :
            return movieslist[size-1]
        else:
            return movieslist[index-1]

def write(**kwargs):
    client = MongoClient("mongodb+srv://pyhackons:pyhackons@cluster0.ajjz3.mongodb.net/crowdengine?retryWrites=true&w=majority")
    db = client['CrowdEngine']
    doc = db['movies']     
    doc.update({'Movies':kwargs['movie']},{ '$set':{'actor':kwargs['actor'],'duration':kwargs['duration'],'role':kwargs['role'],'dresscolor':kwargs['dresscolor'],'target':kwargs['target']} })
    
    
    
def get_csv(a):
       
    client = MongoClient("mongodb+srv://pyhackons:pyhackons@cluster0.ajjz3.mongodb.net/crowdengine?retryWrites=true&w=majority")
    db = client['CrowdEngine']
    doc = db['movies']
    df = list(doc.find({}))
    df = pd.DataFrame(df)
    
    df = df.to_csv('pyhackons-vadivelu-data.csv',index=False)
    path = os.path.abspath('pyhackons-vadivelu-data.csv')
    print(path)
    client.close()
   
    #path = path[:-8] or path.replace('data.csv','')
    path = path.replace('pyhackons-vadivelu-data.csv','')
    a.config["CLIENT_CSV"] = path
    return(send_from_directory(a.config["CLIENT_CSV"],filename='pyhackons-vadivelu-data.csv',as_attachment=True) )
