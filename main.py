from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from prompt import get_response
from redis_con import RedisData

mongo_connection=MongoDB('mongodb://localhost:27017/','zerodha','user','customer_details','report')


app=Flask(__name__)
#creating a instance 
redis_data=RedisData
app.route("/initial",methods=['GET'])
def initial():
    conversation_history=[]

    conversation_history=[{"BOT":"hi,welcome to zerodha ,how can i help you?"}]
    
    redis_data.set_conversation_history("conversation_history",conversation_history)

    return{"message":"hi,welcome to zerodha ,how can i help you?"}


app.route("webbook",methods=['POST'])
def webbook():


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
