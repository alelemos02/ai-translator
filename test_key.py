
import google.generativeai as genai
import os

key = "AIzaSyCwIhNM4cSp0py3GgD48UT0jfEtneCxUeQ"
print(f"Testing key: {key[:5]}...{key[-5:]}")

genai.configure(api_key=key)



try:
    print("Testing gemini-2.0-flash...")
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content("Say 'OK' if you can hear me.")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
