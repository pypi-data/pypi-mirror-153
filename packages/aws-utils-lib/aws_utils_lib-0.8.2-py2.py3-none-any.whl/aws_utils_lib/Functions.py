import json
from pprint import pprint
import boto3
import string
from boto3.dynamodb.conditions import Key
import datetime

def globalSession(profile,table):
    global session
    session=boto3.Session(profile_name=profile)
    global gdb 
    resource=session.resource('dynamodb')
    gdb=resource.Table(table)
    return True

def isession(profile):
    isess=boto3.Session(profile_name=profile)
    return isess


def db(table, **kwargs):
    if "session" in kwargs:
       conn=kwargs["session"]
    else:
        conn=session
 
    resource=conn.resource('dynamodb')
    resource=resource.Table(table)
    return resource

def queryWithIndex(value,key,index,**kwargs):
   
    if "tbname" in kwargs:        
        if "session" in kwargs:
            tb=db(table=kwargs["tbname"],session=kwargs["session"])
        else:
            tb=db(kwargs["tbname"])
    else:
        tb=gdb
    try:
        response= tb.query(
            IndexName=index,
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key(key).eq(value)
        )
        return response
    except:
        raise 

def queryWithKey(value,key,**kwargs):

    if "tbname" in kwargs:        
        if "session" in kwargs:
            tb=db(table=kwargs["tbname"],session=kwargs["session"])
        else:
            tb=db(kwargs["tbname"])
    else:
        tb=gdb
    try:
        response= tb.query(     
            KeyConditionExpression=Key(key).eq(value)
        )
        return response
    except:
        raise 

def putItem(**kwargs):
    if "tbname" in kwargs:        
        if "session" in kwargs:
            tb=db(table=kwargs["tbname"],session=kwargs["session"])
        else:
            tb=db(kwargs["tbname"])
    else:
        tb=gdb
    
    kwargs.pop('tbname',None)
    kwargs.pop('session',None)

    Items=json.dumps(kwargs)
    Items=json.loads(Items)    
    try:
        response= tb.put_item(     
            Item=Items
        )
        return response
    except:
        raise 

def deleteItem(key,value,**kwargs):
    if "tbname" in kwargs:        
        if "session" in kwargs:
            tb=db(table=kwargs["tbname"],session=kwargs["session"])
        else:
            tb=db(kwargs["tbname"])
    else:
        tb=gdb
    try:
        tb.delete_item(     
            Key={
                key:value
            }
        )
        print("Registro eliminado")
    except:
        raise 

def deleteItemWithSortKey(key,value,sortkey,skvalue,**kwargs):
    if "tbname" in kwargs:        
        if "session" in kwargs:
            tb=db(table=kwargs["tbname"],session=kwargs["session"])
        else:
            tb=db(kwargs["tbname"])
    else:
        tb=gdb
    try:
        tb.delete_item(     
            Key={
                key:value,
                sortkey:skvalue
            }
        )
        print("Registro eliminado")
    except:
        raise
def update(partkeyid,value,**kwargs):
    if "tbname" in kwargs:        
        if "session" in kwargs:
            tb=db(table=kwargs["tbname"],session=kwargs["session"])
        else:
            tb=db(kwargs["tbname"])
    else:
        tb=gdb
    datenow=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
    abc =string.ascii_lowercase
    at=""
    ut=""
    ax=0
    index={}
    kwargs.pop('tbname',None)
    kwargs.pop('session',None)

    for key in kwargs.items():
        index[ax]=key[0]
        ax+=1
    ax=0    
    for key in index:
        ut=ut+index[ax] +"=:"+abc[ax]+", "
        ax+=1

    UExp="set "+ut+"UpdatedDate=:zz"
    ax=0    
    for key in index:
        at=at+'":'+abc[ax]+'":"'+kwargs[index[ax]]+'",'
        ax+=1
    EAVal='{'+at+'":zz":"'+datenow+'"}'
    EAVal = json.loads(EAVal)
    try:
        tb.update_item(        
                Key={
                    partkeyid:value
                },
                UpdateExpression=UExp,
                ExpressionAttributeValues=EAVal,
                ReturnValues="UPDATED_NEW"
            )
    except:
        raise
 
def updateWithSortKey(partkeyid,value,sortkeyid,skvalue,**kwargs):
    if "tbname" in kwargs:        
        if "session" in kwargs:
            tb=db(table=kwargs["tbname"],session=kwargs["session"])
        else:
            tb=db(kwargs["tbname"])
    else:
        tb=gdb
    datenow=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
    abc =string.ascii_lowercase
    at=""
    ut=""
    ax=0
    index={}
    kwargs.pop('tbname',None)
    kwargs.pop('session',None)
    for key in kwargs.items():
        index[ax]=key[0]
        ax+=1
    ax=0    
    for key in index:
        ut=ut+index[ax] +"=:"+abc[ax]+", "
        ax+=1

    UExp="set "+ut+"UpdatedDate=:zz"
    ax=0    
    for key in index:
        at=at+'":'+abc[ax]+'":"'+kwargs[index[ax]]+'",'
        ax+=1
    EAVal='{'+at+'":zz":"'+datenow+'"}'
    EAVal = json.loads(EAVal)
    try:
        tb.update_item(        
                Key={
                    partkeyid:value,
                    sortkeyid:skvalue
                },
                UpdateExpression=UExp,
                ExpressionAttributeValues=EAVal,
                ReturnValues="UPDATED_NEW"
            )
    except:
        raise