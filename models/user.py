# models/user.py
class User:
    def __init__(self, user_id, username, role, member_id=None):
        self.user_id = user_id
        self.username = username
        self.role = role          # "Librarian" or "Member"
        self.member_id = member_id

    def is_librarian(self):
        return self.role == "Librarian"

    def __str__(self):
        return f"{self.username} ({self.role})"