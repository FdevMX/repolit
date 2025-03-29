class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class File:
    def __init__(self, id, name, category_id, user_id):
        self.id = id
        self.name = name
        self.category_id = category_id
        self.user_id = user_id

# Additional models can be defined here as needed.