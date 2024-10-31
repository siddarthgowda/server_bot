from flask import Flask, request, jsonify,render_template
from prompt import get_response
from redis_con import RedisData
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from database_code import MongoDB


app=Flask(__name__)

redis_data=RedisData()

mongo_connection = MongoDB('mongodb://localhost:27017/', 'zerodha', 'user', 'customer_details', 'report')


@app.route("/register", methods=['POST'])
def register():
    data = request.json
    print(data)
    username = data.get('username')
    email = data.get('email')
    phonenumber = data.get('phonenumber')
    password = data.get('password')


    if not username or len(username) < 3:
        print("errror:username is to short")
        return jsonify({'error': "Username is too short"})
    
    if not validators.email(email):
        print("errror:email is not vaild!")
        return jsonify({'error': 'Invalid email'})
    
    if not phonenumber or len(phonenumber) != 10:
        print("errror:Phone number must be 10 digits")
        return jsonify({'error': "Phone number must be 10 digits"})
    
    if not password or len(password) < 6:
        print("errror:Password is too short")
        return jsonify({'error': "Password is too short"})
    

    if mongo_connection.find_one({"email": email},collection_type='user'):
        print("errror:Email is already registered")
        return jsonify({'error': 'Email is already registered'})
    
    elif mongo_connection.find_one({"username": username},collection_type='user'):
        print("errror:Email is already registered")
        return jsonify({'error': 'Username is already taken'})

   
    pwd_hash = generate_password_hash(password)
    mongo_connection.insert_one({
        "username": username,
        "password": pwd_hash,   
        "email": email,
        "phonenumber": phonenumber
    },"user")

    return jsonify({"message": "User registered successfully"})


@app.route('/login',methods=['post'])
def login():
    data=request.json
    user=mongo_connection.find_one({'username':data.get('username')},collection_type='user')
    print("User found:", user)
    print("Password provided:", data.get('password'))
    
    if not user or not check_password_hash(user['password'], data.get('password')):
        return jsonify({'message':'invalid username and password'})
    return jsonify({'message':"login sucessful"})


@app.route("/initial",methods=['GET'])
def initial():
    conversation_history=[]
    #find 
    conversation_history=[{"BOT":"hi,welcome to zerodha ,how can i help you?"}]
    
    redis_data.set_conversation_history("conversation_history",conversation_history)

    return{"message":"hi,welcome to zerodha ,how can i help you?"}





@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)


