from flask import *
from model.message import message


messageApi = Blueprint( 'messageApi', __name__)


@messageApi.route('/api/message', methods=['PATCH'])
def message_get():
    return message.messageGet()

@messageApi.route('/api/message', methods=['POST'])
def message_store():
    return message.messageStore()
