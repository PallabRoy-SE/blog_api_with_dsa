from app.plugins import db
from datetime import datetime, timezone


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    # Commenter can be a registered user or null
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    # Define relationship to User model (commenter)
    commenter = db.relationship(
        "User",
        backref=db.backref("comments", lazy="dynamic", cascade="all, delete-orphan"),
    )

    # serialize the Comment
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() + "Z",
            "post_id": self.post_id,
            "user_id": self.user_id,
        }

    def __repr__(self):
        return f"<Comment {self.content[:20]}...>"
