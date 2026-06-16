from flask import Flask, request, jsonify, render_template
from groq import Groq
import os
from dotenv import load_dotenv

from tools import web_search, write_file, read_file
from security import security

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an AI Agent. You can use these tools:
1. web_search(query) - search the web
2. write_file(filename, content) - save to file
3. read_file(filename) - read from file

When asked, decide what to do and respond clearly."""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        
        # Validate input
        validation = security.validate_input(user_message)
        if not validation["safe"]:
            return jsonify({"reply": f"Blocked: {validation['reason']}"})
        
        user_message = validation["cleaned_input"]
        
        # Get Groq's response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        reply = response.choices[0].message.content
        
        # Simple tool detection
        actions = []
        
        if "web_search" in reply.lower() or "search" in reply.lower():
            # Extract query
            query = user_message
            result = web_search(query)
            actions.append(f"✓ Searched for: {query}")
            
            # If asked to save
            if "save" in user_message.lower():
                filename = "search_results.txt"
                content = str(result)
                write_file(filename, content)
                actions.append(f"✓ Saved to: {filename}")
        
        if "read_file" in reply.lower() or "read" in reply.lower():
            filename = "search_results.txt"
            result = read_file(filename)
            actions.append(f"✓ Read file: {filename}")
        
        # Format response
        final_response = reply
        if actions:
            final_response += "\n\nActions:\n" + "\n".join(actions)
        
        return jsonify({"reply": final_response})
    
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)