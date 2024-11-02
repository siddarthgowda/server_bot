from flask import Flask, request, jsonify,render_template
from prompt import get_response
from redis_con import RedisData
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from database_code import MongoDB
import uuid,json
import datetime

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
    elif mongo_connection.find_one({"phonenumber": phonenumber},collection_type='user'):
        print("errror:phonenumber is already registered")
        return jsonify({'error': 'phonenumber is already taken'})

   
    pwd_hash = generate_password_hash(password)
    mongo_connection.insert_one({
        "username": username,
        "password": pwd_hash,   
        "email": email,
        "phonenumber": phonenumber
    },"user")

    mongo_connection.insert_one({
        "username": username,
        "password": pwd_hash,   
        "email": email,
        "phonenumber": phonenumber
    },"customer_details")

    return jsonify({"message": "User registered successfully"})


@app.route('/login',methods=['post'])
def login():
    try:
        data=request.json
        user=mongo_connection.find_one({'username':data.get('username')},collection_type='user')
        print("User found:", user)
        print("Password provided:", data.get('password'))
        
        
        unique=str(uuid.uuid4())
        if not user or not check_password_hash(user['password'], data.get('password')):
            return jsonify({'message':'invalid username and password'})
        
        data=mongo_connection.find_one({"email":json_data.get('email')},collection_type="customer_details")
        unique=json_data.get("unique_id")
        conversation_start=datetime.datetime.now()
        conversation_history=[{"BOT":"hi,welcome to zerodha ,how can i help you?"}]

        redis_data.set_data(unique,{"conversation_history":conversation_history,"user_data":data,"conversation_start":conversation_start})

        #updates=mongo_connection.update_one(cond={'username':user},record={"unique_id":unique},collection_type="customer_details")
        return jsonify({'message':"login sucessful","unique_id":unique})
    except Exception as e:
        print(f"we have a exception as {e}")
        return jsonify({"message":"login failed"})

@app.route("/initial",methods=['GET'])
def initial():
    try: 
        json_data=request.json
        print(f"we are inside initial message{json_data}")

        data=mongo_connection.find_one({"email":json_data.get('email')},collection_type="customer_details")
        unique=json_data.get("unique_id")

        conversation_start=datetime.datetime.now()
        conversation_history=[{"BOT":"hi,welcome to zerodha ,how can i help you?"}]

        redis_data.set_data(unique,{"conversation_history":conversation_history,"user_data":data,"conversation_start":conversation_start})
        
        return jsonify({"message":"hi,welcome to zerodha ,how can i help you?"})
    except Exception as e:
        print(f"we have an exception{e}")
        return jsonify({"message":"hi,welcome to zerodha ,how can i help you?"})



@app.route("/chat",methods=["POST"])
def chat():
    print(f"we have user data as{request.json}")
    try:
        user_text=(request.json).get("user_text")
        unique_id=(request.json).get("unique_id")

        print(redis_data.get_data(unique_id))
        redis_updated_data=redis_data.get_data(unique_id)

        conversation=redis_updated_data.get("conversation_history")
        user_data=redis_updated_data.get("user_data")

        bot_responce=get_response(user_text,conversation,user_data)

        if len(bot_responce.split('|'))>1:
            if bot_responce('|')[1]=='EOC':
                mongo_connection.insert_one(redis_updated_data,collection_type='report')

        conversation.append({'role': 'user', 'content': user_text})
        conversation.append({'role': 'assistant', 'content': bot_responce})
        print(bot_responce)

        return jsonify({"message":bot_responce})
    except Exception as e:
        print(f"we have an exception{e}")
        return {"message":e}



@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)


