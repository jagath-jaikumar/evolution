import uuid

class Animal:
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]