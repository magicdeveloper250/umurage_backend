class User:
    user_id = None
    is_active = False

    def __init__(self, user_id):
        self.user_id = user_id
        self.is_active = True

    def get_id(self):
        return self.user_id
