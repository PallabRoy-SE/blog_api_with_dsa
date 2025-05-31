from app.plugins import db
from app.models.comment import Comment
from datetime import datetime, timezone


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish_date = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship(
        "User",
        backref=db.backref("posts", lazy="dynamic", cascade="all, delete-orphan"),
    )
    comments = db.relationship(
        "Comment", backref="article", lazy="dynamic", cascade="all, delete-orphan"
    )

    def serialize(self, comments=False):
        data = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "publish_date": self.publish_date.isoformat() + "Z",
            "user_id": self.user_id,
            "author_name": (
                f"{self.author.firstname} {self.author.lastname}"
                if self.author
                else None
            ),
        }
        if comments:
            data["comments"] = [
                comment.serialize()
                for comment in self.comments.order_by(Comment.timestamp.asc()).all()
            ]
        return data

    def __repr__(self):
        return f"<Post {self.title}>"
