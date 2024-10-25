from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient


app=Flask(__name__)

client=MongoClient('')
db=client['zerodha_db']
collection=db['user']


    

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
