from flask import *
from model.user import user


userApi = Blueprint( 'userApi', __name__)


@userApi.route("/api/user", methods=["GET"])
def check():
    return user.status()

@userApi.route("/api/user", methods=["POST"])
def signup():
    return user.signup()

@userApi.route("/api/user", methods=["PATCH"])
def signin():
    return user.signin()

@userApi.route("/api/user", methods=["DELETE"])
def signout():
    return user.signout()