import re
from datetime import datetime, timedelta
from collections import defaultdict

class SecurityLayer:
    def __init__(self):
        self.user_requests = defaultdict(list)  # Track requests per user
        self.max_requests_per_minute = 10
        self.blocked_patterns = [
            r"delete",  # Don't allow deletions
            r"drop",    # Don't allow database drops
            r"exec",    # Don't allow code execution
            r"sql injection",
        ]
    
    def validate_input(self, user_input, user_id="default"):
        """Check if user input is safe before agent processes it"""
        
        # 1. Rate limiting - prevent spam
        now = datetime.now()
        self.user_requests[user_id] = [
            req_time for req_time in self.user_requests[user_id]
            if now - req_time < timedelta(minutes=1)
        ]
        
        if len(self.user_requests[user_id]) >= self.max_requests_per_minute:
            return {
                "safe": False,
                "reason": "Too many requests. Please wait."
            }
        
        self.user_requests[user_id].append(now)
        
        # 2. Check for suspicious patterns
        user_input_lower = user_input.lower()
        for pattern in self.blocked_patterns:
            if re.search(pattern, user_input_lower):
                return {
                    "safe": False,
                    "reason": f"Blocked pattern detected: {pattern}"
                }
        
        # 3. Check for prompt injection (common attack)
        injection_patterns = [
            r"ignore.*instructions",
            r"forget.*rules",
            r"pretend.*you.*are",
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, user_input_lower):
                return {
                    "safe": False,
                    "reason": "Potential prompt injection detected"
                }
        
        # 4. Length check
        if len(user_input) > 1000:
            return {
                "safe": False,
                "reason": "Input too long"
            }
        
        if len(user_input) < 2:
            return {
                "safe": False,
                "reason": "Input too short"
            }
        
        # Input is safe
        return {
            "safe": True,
            "cleaned_input": user_input.strip()
        }
    
    def verify_tool_call(self, tool_name, tool_args):
        """Check if agent's tool decision is safe before executing"""
        
        # Dangerous tool combinations
        dangerous_combinations = [
            ("delete_file", "read_file"),  # Delete then read = hiding evidence
            ("write_file", "delete_file"),  # Write then delete = suspicious
        ]
        
        # Check if tool is allowed
        allowed_tools = ["web_search", "write_file", "read_file"]
        if tool_name not in allowed_tools:
            return {
                "safe": False,
                "reason": f"Tool not allowed: {tool_name}"
            }
        
        # Validate tool arguments
        if not tool_args or not isinstance(tool_args, dict):
            return {
                "safe": False,
                "reason": "Invalid tool arguments"
            }
        
        # Tool-specific validation
        if tool_name == "write_file":
            if ".." in tool_args.get("filename", ""):
                return {
                    "safe": False,
                    "reason": "Attempted path traversal in write_file"
                }
        
        if tool_name == "read_file":
            if ".." in tool_args.get("filename", ""):
                return {
                    "safe": False,
                    "reason": "Attempted path traversal in read_file"
                }
        
        # Tool call is safe
        return {
            "safe": True,
            "tool_name": tool_name,
            "tool_args": tool_args
        }
    
    def log_agent_action(self, action_type, details):
        """Log all agent actions for audit trail"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action_type}: {details}\n"
        
        with open("logs/security_audit.log", "a") as f:
            f.write(log_entry)

# Create global security instance
security = SecurityLayer()