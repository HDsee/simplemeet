from flask import *
from model.member import member


memberApi = Blueprint( 'memberApi', __name__)
imgApi = Blueprint( 'imgApi', __name__)



@memberApi.route("/api/member", methods=["POST"])
def member_data_update():
    return member.memberDataUpdate()

@memberApi.route("/api/member", methods=["PATCH"])
def member_search():
    return member.memberSearch()

@imgApi.route("/api/img", methods=["POST"])
def member_img_update():
    return member.memberImgUpdate()
