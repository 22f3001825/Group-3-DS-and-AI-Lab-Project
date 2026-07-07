from flask_login import UserMixin

# In-memory mock user store (prototype)
# Maps email → User object
_users = {}

class User(UserMixin):
    def __init__(self, email):
        self.id    = email
        self.email = email

    @property
    def name(self):
        """Extract student name prefix from IITM email like 22f1000559@ds..."""
        return self.email.split("@")[0]

    @staticmethod
    def get(email):
        return _users.get(email)

    @staticmethod
    def login(email):
        """Create or retrieve a user session object."""
        if email not in _users:
            _users[email] = User(email)
        return _users[email]
