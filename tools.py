from ddgs import DDGS
import os
from datetime import datetime

# Paths
OUTPUTS_DIR = "outputs"
LOGS_DIR = "logs"

# Create directories if they don't exist
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

def log_action(tool_name, input_data, result):
    """Log every tool action for security audit"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Tool: {tool_name} | Input: {input_data} | Result: {result}\n"
    
    with open(f"{LOGS_DIR}/agent_actions.log", "a") as f:
        f.write(log_entry)

def web_search(query):
    """Search the web using DuckDuckGo"""
    # Security: Validate input
    if not query or len(query) == 0:
        return {"error": "Query cannot be empty"}
    
    if len(query) > 500:
        return {"error": "Query too long"}
    
    try:
        results = DDGS().text(query, max_results=5)
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "body": result.get("body", ""),
                "href": result.get("href", "")
            })
        
        log_action("web_search", query, "success")
        return {"results": formatted_results}
    
    except Exception as e:
        log_action("web_search", query, f"error: {str(e)}")
        return {"error": f"Search failed: {str(e)}"}

def write_file(filename, content):
    """Write content to a file in outputs/ folder"""
    # Security: Prevent path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        return {"error": "Invalid filename"}
    
    if not filename.endswith(".txt"):
        filename += ".txt"
    
    # Security: Only write to outputs/ folder
    filepath = os.path.join(OUTPUTS_DIR, filename)
    
    try:
        with open(filepath, "w") as f:
            f.write(content)
        
        log_action("write_file", filename, "success")
        return {"success": f"File saved: {filename}"}
    
    except Exception as e:
        log_action("write_file", filename, f"error: {str(e)}")
        return {"error": f"Write failed: {str(e)}"}

def read_file(filename):
    """Read content from a file in outputs/ folder"""
    # Security: Prevent path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        return {"error": "Invalid filename"}
    
    if not filename.endswith(".txt"):
        filename += ".txt"
    
    # Security: Only read from outputs/ folder
    filepath = os.path.join(OUTPUTS_DIR, filename)
    
    try:
        if not os.path.exists(filepath):
            return {"error": f"File not found: {filename}"}
        
        with open(filepath, "r") as f:
            content = f.read()
        
        log_action("read_file", filename, "success")
        return {"content": content}
    
    except Exception as e:
        log_action("read_file", filename, f"error: {str(e)}")
        return {"error": f"Read failed: {str(e)}"}

# Dictionary of all available tools (agent will choose from these)
AVAILABLE_TOOLS = {
    "web_search": web_search,
    "write_file": write_file,
    "read_file": read_file
}