
import redis
import json

class RedisData:
    def __init__(self):
        self.r = redis.Redis(host="localhost", port=6379, decode_responses=True)

    def set_conversation_history(self, key, conversation_history): 
        self.r.set(key, json.dumps(conversation_history)) 

    def setex_checking_history(self, key, conversation_history):
        self.r.setex(key, 60, json.dumps(conversation_history))
 
    def get_conversation_history(self, key):
        conversation_history = self.r.get(key)
        if conversation_history:
            return json.loads(conversation_history)
        return []
