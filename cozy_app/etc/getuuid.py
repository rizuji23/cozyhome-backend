import uuid

class Ramdom_Id:
    @staticmethod
    def get_id():
        return str(uuid.uuid4())[:8]