from app.plugins import db
from app.utils import get_password_hash, check_password


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(64), index=True, nullable=False)
    lastname = db.Column(db.String(64), index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # set password to the user
    def set_password(self, password: str):
        self.password = get_password_hash(password)

    # check password is valid or not
    def check_password(self, password: str) -> bool:
        return check_password(password, self.password)

    # serialize the User
    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }

    def __repr__(self):
        return f"<User {self.firstname} {self.lastname}, Email {self.email}>"
