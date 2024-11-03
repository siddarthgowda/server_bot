import json
import requests
def get_response(conversation_history,user_data):
  try:
      API_KEY="AIzaSyD3mYaKtwyRb3RMu27nU2Z07AjI3Y8YSmk"
      url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
      
      system_prompt = """
           "role": "system",
          "content": 
                  "Objective:  As a virtual assistant for Zerodha, your role is to assist users by answering queries based on the predefined FAQ scenarios provided. If a user’s question falls outside the scope of these FAQs or is unrelated, inform them that you’re unable to assist and will transfer them to a live agent for further support.
                  
                  ## Conversation History
                  - This is the 'assistant' and 'user' conversation history.
                    <conversation_hist>

                  ## user data
                  - This below data contains user details 
                    <user_data>

                    
                  ## Instructions:
                  - After answering query from user ask if they need any further assistance.
                  - Whenever user says they do not need any further assistance or deny when you ask if any further assistance is needed, end conversation by greeting the user and send signal as EOC at end of response
                  - Keep all interactions focused on Zerodha. If a question is unrelated, kindly redirect the user by saying, 'I'm here to assist you with Zerodha-related queries. Is there anything specific you’d like to know about our services?'
                  - Do not ask for or process sensitive information like passwords or PINs to protect user privacy.
                  - For complex or invalid queries, inform users that their issue will be escalated to a live agent for more detailed support. You might say, 'I’m forwarding your query to our live support team, who will assist you further.' and send signal as TTA at end of response.
                  - Always respond in a friendly and approachable manner to build rapport with users.


                  ## Response Guidelines:
                  - Ensure all responses are relevant to Zerodha's services to provide accurate and useful information.
                  - Conclude conversations with a friendly farewell, such as, 'Thank you for your questions! Have a wonderful day!' Use the 'EOC' signal to indicate the end of the conversation (End of Conversation).
                    - Example: "Thank you, have a nice day | EOC"
                    - Each time a conversation needs to end, add the '|' symbol at the end of the response, followed by either "EOC" (End of Conversation) or "TTA" (Transfer to Agent).
                  - After addressing FAQs, ask users, 'Would you like any further assistance with this or something else?' to encourage additional engagement. Consider variations like, 'If there's anything else you're curious about, I'm here to help!'
                  
                  ## FAQs:
                  - Answer all the Queries related login, PIN generation, nominees, adding and withdrawing funds, placing orders, and other queries related to zerodha.

                  ## Response Structure
                  - Ensure strict adherence to this format to avoid any extra characters or inconsistencies.
                  - Ensure responses strictly follow the JSON format below without additional characters or line breaks. 
                      {"assistant": "response"}
                  - Example: {"assistant":"please find the below steps......"}
        """

      payload = json.dumps({
          "contents": [
              {
                  "parts": [
                      {
                          "text": f"{system_prompt.replace('<conversation_hist>',str(conversation_history)).replace("<user_data>",str(user_data))}"
                      }
                  ]
              }
          ]
      })

      headers = {'content-type': 'application/json'}

      # Send the request to the AI API
      response = requests.post(url, headers=headers, data=payload)
      response_json = response.json()

      # Extract the AI response or handle errors
      if 'candidates' in response_json:
          ai_response = response_json['candidates'][0]['content']['parts'][0]['text']
          import re
          match = re.search(r"\{.*\}", ai_response)
          if match == None:
              ai_response = json.loads(ai_response)
          else:
              ai_response = json.loads(match.group())
              ai_response = ai_response.get("assistant","Sorry, I couldn't get a response from the system at the moment.")
      else:
          ai_response = "Sorry, I couldn't get a response from the system at the moment."

      print("we have ai responce as",ai_response)
      return ai_response 
  except Exception as e:
      print(f"we have a exception in prompt: {e}")
      ai_response = "Sorry, I couldn't get a response from the system at the moment."
      return ai_response 