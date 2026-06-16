# AI Agent - Level 4

A working AI Agent with tool use, built from scratch with Groq API.

## Features

- ✅ Agentic AI (agent decides which tools to use)
- ✅ Web search tool
- ✅ File read/write tools
- ✅ Security layer (input validation, output verification, audit logging)
- ✅ Web interface with Flask
- ✅ Conversation logging

## What is an AI Agent?

An AI agent is not a chatbot. It:
- **Thinks** about your request
- **Decides** which tools it needs
- **Executes** those tools in order
- **Adapts** based on results
- **Reports** what it did

## How to use

### Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

Then open browser: `http://localhost:5000`


### Try these commands

1. **Direct questions (no search):**
Tell me about Python programming

2. **Save to file:**
Explain machine learning and save it to a file

3. **Read file:**
Read the file I just saved

4. **Complex explanation:**
Explain what is artificial intelligence in detail and save to ai_explained.txt

5. **Code-related:**
What are the best practices for Python development?

**Note:** The agent can answer directly from its training or search the web. If you ask it to search, it may return limited results due to API constraints. The agent is smart enough to use its knowledge when search returns nothing.

chatbot-agent/

├── app.py              # Flask + Agent loop

├── tools.py            # Tool definitions (search, write, read)

├── security.py         # Input validation + audit logging

├── requirements.txt    # Dependencies

├── .gitignore          # Files to ignore

├── README.md           # This file

├── templates/

│   └── index.html      # Web interface

├── outputs/            # Where files are saved (sandboxed)

└── logs/               # Agent action logs


## How it works

### The Agent Loop

User: "Explain Python and save"

↓

Security validates input

↓

Groq receives request + available tools

↓

Groq decides what to do

↓

Flask executes the tools (if needed)

↓

Groq receives results

↓

Agent returns final response


### Security Features

1. **Limited tools** — Agent can only use predefined tools
2. **Input validation** — Blocks malicious input
3. **Output verification** — Checks tool calls before executing
4. **Sandboxing** — Files only saved to `outputs/` folder
5. **Audit logging** — Every action logged for debugging

## Key learnings

- How AI agents actually work (not scripted, truly agentic)
- Function calling (how Groq decides which tool to use)
- Tool use design pattern
- Security in agentic systems
- Building multi-step autonomous workflows

## Tech stack

- **Python 3.14.3**
- **Flask** — Web server
- **Groq API** — AI model (llama-3.3-70b)
- **DDGS** — Web search
- **SQLite** — Logging

## File breakdown

**app.py** — Main Flask server + agent loop
- Handles web requests
- Manages agent decision loop
- Executes tools based on agent decisions

**tools.py** — Available tools for agent
- `web_search()` — Search the web
- `write_file()` — Save to disk
- `read_file()` — Read from disk

**security.py** — Security layer
- Input validation (blocks bad input)
- Tool verification (checks before executing)
- Audit logging (records all actions)

**index.html** — Web interface
- Chat box for user commands
- Displays agent responses
- Shows actions taken

## Future improvements

- Add conversation memory
- Deploy online 
- Build API for other apps 
- Add more tools (calculator, code execution, etc.)
- Better error handling

## Author

Divyam Mishra
GitHub: divmishra476-bit
