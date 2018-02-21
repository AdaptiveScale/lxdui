from flask import jsonify, make_response

def replySuccess(data=None, message='Success'):
    return make_response(jsonify({'status':200,'message':message,'data':data}), 200)

def replyFailed(data=None, message='Failed', status=403):
    return make_response(jsonify({'status':status, 'message':message,'data':data}), status)

def reply(data=None, message='Success', status=200):
    if status in [200]:
        return replySuccess(data, message)
    else:
        return replyFailed(data=data, message=message, status=status)