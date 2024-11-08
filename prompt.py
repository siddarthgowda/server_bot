
import json
import requests

def get_response(conversation_history, user_data):
    try:
        API_KEY = "AIzaSyD3mYaKtwyRb3RMu27nU2Z07AjI3Y8YSmk"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
        
        system_prompt = """
                    "role": "system",
                    "content": 
                        "Objective: As a knowledgeable and empathetic virtual assistant for Zerodha, actively listen to user queries, understand their needs, and provide tailored solutions or politely inform them of limitations.
                        ## Conversation History
                        - This section contains the conversation history. Refer to it to ensure continuity and avoid redundant questions.
                        <conversation_hist>

                        ## User Data
                        - This section contains user-specific details:
                        <user_data>

                        ## Instructions:
                        - Avoid requesting sensitive data from the user, such as T-PIN or account details.
                        - Provide concise answers with clear steps, avoiding repetition.
                        - After answering the user's query, ask, 'Is there anything else I can help you with?'
                        - If the user responds with "no" or similar:
                            1. Acknowledge their response (e.g., 'Thank you for reaching out to Zerodha. Have a great day!').
                            2. Close the conversation with "EOC" without repeating any previous responses.
                        - If the user responds with "yes," prompt them with a follow-up question like, 'Please let me know how else I can assist.'
                        



                        
                        ## Transfer Protocol
                        - If the user's query is outside the scope of FAQs, inform them that you'll transfer the chat to a live agent, politely ask the user to wait, and use the "TTA" signal.
                        
                        ## Flow Structure
                        - Greet the user warmly and professionally.
                        - Actively listen to the user's query, asking clarifying questions if needed.
                        - Provide a clear, concise, and helpful response, drawing from the FAQs or your knowledge base.
                        - Always refer to the conversation history before answering to maintain continuity.
                        - Follow this flow:
                            - Answer user queries.
                            - Confirm if further help is needed.
                            - Prompt the user if they say "yes" by asking how you can assist.
                            - If no further help is needed, close with a thank-you message and "EOC" without repeating any response.
                            - For outside-scope queries, transfer the conversation with a greeting and "TTA."
                        
                        ## FAQs
                        - Specific FAQs you can answer include: 
                            - Login/logout steps
                            - Adding and withdrawing funds
                            - Changing PIN
                            - Order steps (buy/sell)
                            - IPO application and general questions
                            - GTT and MTF order queries
                            - Nominee management
                            - make sure you go through the process for to check account status below:
                            1. Ask the user to provide their phone number.
                            2. Ask the user for their OTP.
                            3. Validate the provided phone number and OTP against 'user_data' for verification.
                            
                            
                        - Use the correct response format with 'EOC' or 'TTA' signals as needed.
                    """


# - Account status (verify with phone number and PIN):
#                                 - For Account status, verify the user by asking user their phone_number and PIN and then validating it with 'user_data'

        payload = json.dumps({
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{system_prompt.replace('<conversation_hist>', str(conversation_history)).replace('<user_data>', str(user_data))}"
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
            ai_response = ai_response.replace("Assistant: ","").replace("assistant:","").replace("assistant:","").replace("Assistant Assistant:","")
            # print(ai_response)
            # import re
            # match = re.search(r"\{.*\}", ai_response)
            # if match is None:
            #     ai_response = json.loads(ai_response)
            # else:
            #     ai_response = json.loads(match.group())
            #     ai_response = ai_response.get("assistant", "Sorry, I couldn't get a response from the system at the moment.")
        else:
            ai_response = "Sorry, I couldn't get a response from the system at the moment."

        print("Assistant", ai_response)
        return ai_response 

    except Exception as e:
        print(f"We have an exception in prompt: {e}")
        ai_response = "Sorry, I couldn't get a response from the system at the moment."
        return ai_response
