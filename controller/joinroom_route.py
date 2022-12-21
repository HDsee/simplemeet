from flask import *
from model.joinroom import joinroom


joinroomApi = Blueprint( 'joinroomApi', __name__)


@joinroomApi.route('/api/joinroom', methods=['GET'])
def check():
    return joinroom.roomStatus()

@joinroomApi.route('/api/joinroom', methods=['PATCH'])
def signup():
    return joinroom.roomIn()

@joinroomApi.route('/api/joinroom', methods=['DELETE'])
def signin():
    return joinroom.roomOut()
