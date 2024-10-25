import json
import requests


def get_response(user_input, conversation_history):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=YOUR_API_KEY"
    
    
    system_prompt = '''{
        "role": "system",
        "content": "Objective: As an AI assistant at Zerodha, your role is to engage with customers and address all their queries related to any issues with Zerodha's services. 
                    
                    ## Instructions: 
                    - Redirect any off-topic questions back to Zerodha-related queries to ensure the conversation stays relevant to Zerodha services. 
                    - Avoid requesting sensitive account details (such as passwords or PINs) and refrain from guiding customers through payment processes directly. 
                    - If the user has no further queries, ask at the end if there is anything else you can assist with. 
                    - If the user inputs an invalid or overly complex query, inform them that their issue will be transferred to a live agent for further assistance. 
                    
                    ## Response Guidelines: 
                    - Review and ensure that responses address only queries relevant to Zerodha's services. 
                    - When ending conversations, include a closing greeting and send the 'EOC' signal to mark the end of the conversation. 
                    - After answering any FAQs, continue the conversation by asking if 'Would you like any further assistance with this or something else?'. 
                    - If a query is too complex or falls outside the scope of the bot's capabilities, politely inform the user that their request will be forwarded to a live agent for further assistance. 
                   
                     ## FAQs: 
                    - 'How to add funds on Zerodha?' 'Adding funds on Zerodha is easy! Just follow the steps that will be sent to you via SMS after this call. Can I help you with anything else?' 
                    - 'How to withdraw funds in Zerodha?' 'Withdrawing funds from Zerodha is quick and easy! You can use our Instant Withdrawal facility, and the process will be completed within 15 minutes. A step-by-step guide will be sent to you via SMS after this call. Is there anything else I can assist you with?' 
                    - 'Why is my fund balance lower than expected?' 'You are seeing a lower fund balance due to the Quarterly Settlement process mandated by the Exchange. I'll send you more details about this via SMS after this call. Is there anything else I can assist you with?' 
                    - 'What is a quarterly settlement, and how does it affect my account?' 'You're seeing a lower fund balance due to the Quarterly Settlement process mandated by the Exchange. I'll send you more details about this via SMS after this call. Is there anything else I can assist you with?' 
                    - 'How do I add a new bank account in Zerodha?' 'Sure, I can help you with this. I'll send you more details about adding a bank account via SMS after this call. Is there anything else I can assist you with?' 
                    - 'How do I add a nominee in Zerodha?' 'I will send an SMS after this call with detailed steps on how to generate a TPIN. Please check your messages for the instructions. Do you need any further assistance?' 
                    - 'How do I edit a nominee in Zerodha?' 'Sure, I can help you modify a nominee in your Zerodha account. Please refer to our SMS for a step-by-step guide on how to modify a nominee.'"
    }'''
    # Append the user input to conversation history
    conversation_history.append({'role': 'user', 'content': user_input})

    # Prepare the conversation text for API request
    history_text = ''.join([f"{entry['role']}: {entry['content']} " for entry in conversation_history])

    payload = json.dumps({
        "contents": [
            {
                "parts": [
                    {
                        "text": f"{system_prompt}\n\n{history_text}"
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
    else:
        ai_response = "Sorry, I couldn't get a response from the system at the moment."

    # Truncate the response if necessary (example: max 50 words)
    ai_response_words = ai_response.split()
    if len(ai_response_words) > 50:
        ai_response = ' '.join(ai_response_words[:50]) + "..."

    # Append the AI response to the conversation history
    conversation_history.append({'role': 'assistant', 'content': ai_response})
    
    return ai_response
