from flask import *
from model.friend import friend


friendApi = Blueprint( 'friendApi', __name__)


@friendApi.route("/api/friend", methods=["GET"])
def friend_get():
    return friend.friendGet()

@friendApi.route("/api/friend", methods=["POST"])
def friend_join():
    return friend.friendJoin()
