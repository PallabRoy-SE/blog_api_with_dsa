from app.plugins import db
from flask import Blueprint, request, jsonify
from app.models import User, Post, Comment
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, Unauthorized

blog_bp = Blueprint("blog_api", __name__, url_prefix="/api")


# get all posts with pagination
@blog_bp.route("/posts", methods=["GET"])
def get_all_posts():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    paginated_posts = Post.query.order_by(Post.publish_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return (
        jsonify(
            {
                "posts": [post.serialize() for post in paginated_posts.items],
                "total_posts": paginated_posts.total,
                "total_pages": paginated_posts.pages,
                "current_page": paginated_posts.page,
            }
        ),
        200,
    )


# get a post by id
@blog_bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id: int):
    post = db.session.get(Post, post_id)
    if not post:
        raise NotFound("Post not found")
    return jsonify(post.serialize(comments=True)), 200


# create a new post
@blog_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user:
        raise Unauthorized("User not found or token invalid")

    data = request.get_json()
    if not data or not data.get("title") or not data.get("content"):
        raise BadRequest("Missing title or content")

    post = Post(title=data["title"], content=data["content"], author=user)
    db.session.add(post)
    db.session.commit()

    return (
        jsonify({"message": "Post created successfully", "post": post.serialize()}),
        201,
    )


# update or delete a post by id
@blog_bp.route("/posts/<int:post_id>", methods=["PUT", "DELETE"])
@jwt_required()
def modify_delete_post(post_id):
    current_user_id = get_jwt_identity()
    if current_user_id:
        current_user_id = int(current_user_id)
    post = db.session.get(Post, post_id)

    if not post:
        raise NotFound("Post not found")
    if post.user_id != current_user_id:
        raise Forbidden("You are not authorized to make changes on this post")

    if request.method == "PUT":
        data = request.get_json()
        if not data:
            raise BadRequest("No data provided for update")

        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        db.session.commit()

        return (
            jsonify({"message": "Post updated successfully", "post": post.serialize()}),
            200,
        )
    elif request.method == "DELETE":
        db.session.delete(post)
        db.session.commit()

        return jsonify({"message": "Post deleted successfully"}), 200
    else:
        raise Forbidden("Method is Not Allowed")


# get comments for a post
@blog_bp.route("/posts/<int:post_id>/comments", methods=["GET"])
def get_comments(post_id: int):
    post = db.session.get(Post, post_id)
    if not post:
        raise NotFound("Post not found")

    comments = post.comments.order_by(Comment.timestamp.asc()).all()

    return jsonify([comment.serialize() for comment in comments]), 200


# add comment for a post
@blog_bp.route("/posts/<int:post_id>/comments", methods=["POST"])
@jwt_required(optional=True)
def add_comment(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        raise NotFound("No post found to comment")

    data = request.get_json()
    if not data or not data.get("name") or not data.get("content"):
        raise BadRequest("Name and content is required to comment")

    comment = Comment(
        name=data["name"],
        content=data["content"],
        post_id=post.id,
        user_id=int(get_jwt_identity()) if get_jwt_identity() else None,
    )
    db.session.add(comment)
    db.session.commit()

    return (
        jsonify(
            {"message": "Comment added successfully", "comment": comment.serialize()}
        ),
        201,
    )


# Blueprint specific error handlers
@blog_bp.app_errorhandler(BadRequest)
def handle_post_bad_request(e):
    return jsonify(error=str(e.description) if e.description else "Bad Request"), 400


@blog_bp.app_errorhandler(Forbidden)
def handle_post_forbidden(e):
    return jsonify(error=str(e.description) if e.description else "Forbidden"), 403


@blog_bp.app_errorhandler(NotFound)
def handle_post_not_found(e):
    return (
        jsonify(error=str(e.description) if e.description else "Not found"),
        404,
    )
