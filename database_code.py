from pymongo import MongoClient
from bson import ObjectId

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
        

    def update_one(self,cond,record,collection_type):
        try:
            if collection_type=="user":
                collection=self.user
            elif collection_type=="customer_details":
                collection=self.customer_details
            elif collection_type=="report":
                collection=self.report
            
            db=self.client[collection]

            if '_id' in record:
                record=convert_bson_Id(record)

            if '_id' in cond:
                cond=convert_bson_Id(cond)

            result=db.update_one(cond,{"$set":record})
            print("customer_details and report are updated",result)
        except Exception as e:
            print("Exception error as {e}")


    def insert_one(self, record, collection_type):
        try:
            if collection_type == "user":
                collection = self.user
            elif collection_type == "customer_details":
                collection = self.customer_details
            elif collection_type == "report":
                collection = self.report
            
            db = self.client[collection]

            if '_id' in record:
                record = convert_bson_Id(record)

            result = db.insert_one(record)
            print("report successfully updated", result)
        except Exception as e:
            print("Exception error as {e}")


    
    
    def remove_one(self,cond,collection_type):
        try:
            if collection_type=="user":
                collection=self.user
            elif collection_type=="customer_details":
                collection=self.customer_details
            elif collection_type=="report":
                collection=self.report
            
            db=self.client[collection]

            if 'id' in cond:
                cond=convert_bson_Id(cond)


            #if 'id' in record:
               # record=convert_bson_Id(record)

            result=db.delete_one(cond)
            print("users removed sucessfully ",result.deleted_count)
        except Exception as e:
            print("Exception error as {e}")


    def find_one(self,cond,collection_type):
        try:
            if collection_type=="user":
                collection=self.user
            elif collection_type=="customer_details":
                collection=self.customer_details
            elif collection_type=="report":
                collection=self.report
            
            db=self.client[collection]
 
            if '_id' in cond:
                cond=convert_bson_Id(cond)

            result=db.find_one(cond)
            print(result)
            return result
        except Exception as e:
            print("Exception error as {e}")
            return None

    def find(self,cond,collection_type):
        try:
            if collection_type=="user":
                collection=self.user
            elif collection_type=="customer_details":
                collection=self.customer_details
            elif collection_type=="report":
                collection=self.report
            
            db=self.client[collection]

            if '_id' in cond:
                cond=convert_bson_Id(cond)

            result=db.find(cond)
            print(result)
            
            for document in result:
                print(document)
        except Exception as e:
            print("Exception error as {e}")
    

    
    
if __name__=='__main__':
    mongo_connection=MongoDB('mongodb://localhost:27017/','zerodha','user','customer_details','report')
    

    #mongo_connection.insert_one({"name":"siddarth","phone_number":9113650004,"status":"active"},"user")
    #mongo_connection.insert_one({"name":"sagar","age":27,"status":"active"},"customer_details")
    #mongo_connection.insert_one({"name":"siddarth","age":"","status":"active"},"user")
    #mongo_connection.update_one({"name":"siddarth"},{"phone_number":9482065549},"user")
    #mongo_connection.remove_one({"name":"varsha"},"user")
    #mongo_connection.remove_one({'_id':ObjectId('671f84e9bc9c7f84f9c4605e')},'user')
    #mongo_connection.find_one({'name':'siddarth'},'user')
    #mongo_connection.find({'age':{'$lte':18}},'customer_details')
    #mongo_connection.find({}, 'user')
    