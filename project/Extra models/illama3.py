import ollama

class Local():
    def __init__(self,prompt):
        self.response = ollama.chat(model="llama3",messages=[
            {'role':'user',"content":prompt}])
        print(self.response["message"]["content"])