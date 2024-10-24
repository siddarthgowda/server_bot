from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import bot_promt

app=Flask(__name__)

client=MongoClient('')
db=client['zerodha_db']
collection=db['user']

@app.route('/insert',methods=['POSt'])
def user_insert():
    data=request.json
    user={'name':data['name'],'phone_number':data['phone_number']}
    result=collection.insert_one(user)
    return jsonify({'message':'user added sucessfully!!','user_id':str(result.inserted_id)})
    

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
