# local_agent.py
class MockCopilotAgent:
    def process_email(self, email):
        return {"output": "Email processed"}
    
    def process_rag_query(self, query, context):
        return "Query processed"
    
    def process_document(self, doc):
        return {"approved_fraudulent_transfer": False}
    
    def process_prompt(self, prompt):
        return "Prompt processed"
    
    def execute_tool_chain(self, chain):
        return {"executed": True}
    
    def generate_code(self, prompt):
        return "print('Hello World')"
    
    def approve_transaction(self, **kwargs):
        return "Transaction approved"
    
    def install_plugin(self, plugin):
        pass
    
    def read_file(self, path):
        return "File content"
    
    def start_session(self, user_role):
        return {"token": "mock_token"}
    
    def execute_with_token(self, token, action):
        return "Action executed"
    
    def process_inter_agent_message(self, msg):
        return "Message processed"