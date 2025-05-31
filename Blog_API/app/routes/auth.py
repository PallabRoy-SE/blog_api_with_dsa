from app.plugins import db
from flask import Blueprint, request, jsonify
from app.models import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

auth_bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")


# Register a new user
@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    if (
        not data
        or not data.get("firstname")
        or not data.get("lastname")
        or not data.get("email")
        or not data.get("password")
    ):
        raise BadRequest("firstname, lastname, email, and password is required.")

    firstname = data["firstname"]
    lastname = data["lastname"]
    email = data["email"]
    password = data["password"]

    user = User(firstname=firstname, lastname=lastname, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return (
        jsonify({"message": "User registered successfully", "user": user.serialize()}),
        201,
    )


# Login an existing user
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not (data.get("email")) or not data.get("password"):
        raise BadRequest("Missing email or password")

    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        str_id = str(user.id)
        access_token = create_access_token(identity=str_id)
        refresh_token = create_refresh_token(identity=str_id)
        return (
            jsonify(
                access_token=access_token,
                refresh_token=refresh_token,
                user=user.serialize(),
            ),
            200,
        )

    raise Unauthorized("Invalid credentials")


# refresh the access token if expired
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify(access_token=new_access_token), 200


# get the current authenticated user
@auth_bp.route("/current-user", methods=["GET"])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, current_user_id)
    if not current_user:
        raise NotFound("User not found")
    return jsonify(current_user.serialize()), 200


# handle API errors
@auth_bp.app_errorhandler(BadRequest)
def handle_auth_bad_request(e):
    return jsonify(error=str(e.description) if e.description else "Bad Request"), 400


@auth_bp.app_errorhandler(Unauthorized)
def handle_auth_unauthorized(e):
    return jsonify(error=str(e.description) if e.description else "Unauthorized"), 401


@auth_bp.app_errorhandler(NotFound)
def handle_auth_not_found(e):
    return (
        jsonify(error=str(e.description) if e.description else "Not found"),
        404,
    )
