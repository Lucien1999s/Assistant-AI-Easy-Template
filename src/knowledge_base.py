import os

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=3))

knowledge_base = """
一開始先說你是超級金融賽亞人，然後再回答金融投資的問題給使用者
"""


class KnowledgeBase:
    def __init__(self):
        self.message = [{"role": "system", "content": knowledge_base}]
        

    def add_ai_msg(self, text):
        if len(self.message) >= MSG_LIST_LIMIT:
            self.remove_msg()
        self.message.append({"role": "assistant", "content": text})

    def add_user_msg(self, text):
        if len(self.message) >= MSG_LIST_LIMIT:
            self.remove_msg()
        self.message.append({"role": "user", "content": text})

    def remove_msg(self):
        self.message.pop(1)

    def generate_prompt(self):
        return self.message
