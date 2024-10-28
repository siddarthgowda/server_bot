from pymongo import MongoClient
from bson import ObjectId

#client=MongoClient('mongodb://localhost:27017/')
#db=client['zerodha']
#user_collection=db['user']
#customer_collection=db['customer_details']
#report_collection=db['report']
#'mongodb://localhost:27017/','zerodha','user','customer_details','report'

#update_one
#insert_one 
#delete
#find_one 
#find

url=('mongodb://localhost:27017/')
client=MongoClient(url)['database']['collections']

def convert_bson_Id(record):
    record['_id']=ObjectId(record['_id'])



class MongoDB:
    def __init__(self,url,db,user,customer_details,report):
        self.user=user
        self.customer_details=customer_details
        self.report=report


        self.client=MongoClient(url)[db]
        

    def update_one(self,customer_details,report,collection_type):
        try:
            if collection_type=="user":
                collection=self.user
            elif collection_type=="customer_details":
                collection=self.customer_details
            elif collection_type=="report":
                collection=self.report
            
            db=self.client[collection]


            #if '_id' in condition:
                #condition=convert_bson_Id(condition)

            if '_id' in record:
                record=convert_bson_Id(record)

            result=db.update_one({"$set":record})
            print("customer_details and report are updated",result)
        except Exception as e:
            print("Exception error as {e}")


    def insert_one(self,record,collection_type):
        try:
            if collection_type=="user":
                collection=self.user
            elif collection_type=="customer_details":
                collection=self.customer_details
            elif collection_type=="report":
                collection=self.report
            
            db=self.client[collection]

            if 'id' in record:
                record=convert_bson_Id(record)

            result=db.insert_one(record)
            print("report sucessfully  updated",result)
        except Exception as e:
            print("Exception error as {e}")

    
    
    def remove_one(self,record,collection_type):
        try:
            if collection_type=="user":
                collection=self.user
            elif collection_type=="customer_details":
                collection=self.customer_details
            elif collection_type=="report":
                collection=self.report
            
            db=self.client[collection]

            if 'id' in record:
                record=convert_bson_Id(record)

            result=db.delete_one(record)
            print("users removed sucessfully ",result)
        except Exception as e:
            print("Exception error as {e}")

    def find_one(self,user,collection_type):
        try:
            if collection_type=="user":
                collection=self.user
            elif collection_type=="customer_details":
                collection=self.customer_details
            elif collection_type=="report":
                collection=self.report
            
            db=self.client[collection]

            if 'id' in record:
                record=convert_bson_Id(record)

            result=db.find_one(record)
            print(result)
        except Exception as e:
            print("Exception error as {e}")
    

    def find(self,user,customer_details,report,collection_type):
        try:
            if collection_type=="user":
                collection=self.user
            elif collection_type=="customer_details":
                collection=self.customer_details
            elif collection_type=="report":
                collection=self.report
            
            db=self.client[collection]

            if 'id' in record:
                record=convert_bson_Id(record)

            result=db.find(record)
            print(result)
        except Exception as e:
            print("Exception error as {e}")
    

    
    
if __name__=='__main__':
    mongo_connection=MongoDB('mongodb://localhost:27017/','zerodha','user','customer_details','report')
    

    