from pymongo import MongoClient

client=MongoClient('mongodb://localhost:27017/')
db=client['zerodha']
user_collection=db['user']#name,password
customer_collection=db['customer_details']#name rgister mobile,opt, status 
report_collection=db['report']

#find_one
#find
#insert_one
#delete
#update


def insert_user(self,user):
    try:
        data={"user_name":user.user_name,"password":user.password}
        result=self.user_collection.insert_one(data)
        print(f"user inserted with id :{result.inserted_id}")
    except Exception as e:
        print(f"error:{e}")

def insert_customer_details(self,customer_details):
    try:
        data={"user_name":customer_details.user_name,"number":customer_details.number,"OTP":customer_details.OTP,"pofile_status":customer_details.profile_status}
        result=self.customer_collection.insert_one(data)
        print(f"customer_details inserted with id :{result.inserted_id}")
    except Exception as e:
        print(f"error:{e}")


##

class MongoDB:

    def _init_(self):
        try:
            self._mongo_db = self._database_config["mongo_api"]["zerodha"]

            self.user_collection = self._database_config["mongo_api"]["user"]
            self.customer_collection = self._database_config["mongo_api"]["customer_details"]
            self.report_collection = self._database_config["mongo_api"]["report"]


            port = "5001
            url = "mongodb://localhost:27017/”
            self.mongo_url = “ ”
            # logger.info(self.mongo_url)
            self.connect()
            

        except Exception as e:
            print("Exception while loading the config-->" + str(e))

    def connect(self,col_type=""):
        try:
            if read:
                self.mongo_conn_read = MongoClient(self.mongo_url)
                self.user_collection_read = self.mongo_conn_read[self.zerodha][self.user_collection]
                return self.user_collection_read
