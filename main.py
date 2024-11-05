from flask import Flask, request, jsonify,render_template
from prompt import get_response
from redis_con import RedisData
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from database_code import MongoDB
import uuid
import json
import datetime

app=Flask(__name__)

redis_data=RedisData()


mongo_connection = MongoDB('mongodb://localhost:27017/', 'zerodha', 'user', 'customer_details', 'report')

def list_to_string(conversation):
    """Converts a list of conversation messages into a single string."""
    formatted_conversation = []
    for item in conversation:
        if 'user' in item:
            formatted_conversation.append(f"user: {item['user']}")
        if 'assistant' in item:
            formatted_conversation.append(f"Assistant: {item['assistant']}")
    return "\n".join(formatted_conversation)


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
        user=data.get("username")
        password=data.get("password")
        user_data=mongo_connection.find_one({'username':user},collection_type='user')
        print("User found:", user)
        print("Password provided:", password)
        
        
        unique=str(uuid.uuid4())
        if not user or not check_password_hash(user_data['password'], data.get('password')):
            return jsonify({'message':'invalid username and password'})
        
        updates=mongo_connection.update_one(cond={'username':user},record={"unique_id":unique},collection_type="customer_details")
        print(updates)
        print({'message':"login sucessful","unique_id":unique})
        return jsonify({'message':"login sucessful","unique_id":unique})
    except Exception as e:
        print(f"we have a exception as {e}")
        return jsonify({"message":"login failed"})



@app.route("/initial",methods=['POST'])
def initial():
    try: 
        json_data=request.json

        unique=json_data.get("unique_id")

        data=mongo_connection.find_one({"unique_id":unique},collection_type="customer_details")

        if '_id' in data:
            del data['_id']

        conversation_start=str(datetime.datetime.now())
        conversation_history=[{"assistant":"Hey, Welcome to zerodha ,how can i help you?"}]

        redis_data.setex_set_data(unique,{"conversation_history":conversation_history,"user_data":data,"conversation_start":conversation_start})
        
        return jsonify({"message":"Hey,welcome to zerodha ,how can i help you?"})
    except Exception as e:
        print(f"we have an exception{e}")
        return jsonify({"message":"please login before you use the chat"})



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
        conversation.append({'user': user_text})

        conversation_htx = list_to_string(conversation)
        print(f"Current conversation as string:\n{conversation_htx}")

        
        api_responce=get_response(conversation,user_data)
        bot_responce=api_responce

        if len(bot_responce.split('|'))>1:
            if bot_responce('|')[1] in ['EOC','TTA']:
                mongo_connection.insert_one(redis_updated_data,collection_type='report')

        conversation.append({'assistant': bot_responce})

        new = {"conversation_history":conversation}
        new_data = {**redis_updated_data,**new}

        redis_data.setex_set_data(unique_id,new_data)

        return jsonify({"message":bot_responce})
    
    except Exception as e:
        print(f"we have an exception in chat as ---> {str(e)}")
        return {"message": str(e)}



@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True,port=5002)


