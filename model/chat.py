from flask import session, jsonify
from flask_socketio import emit, join_room, leave_room, Namespace
from datetime import datetime
import random
from queue import Queue

cnt = 0
cnt_to_mbti = {}

def socketio_init(socketio):
    guest_number = str(random.randrange(1000, 10000))

    @socketio.on('joined', namespace='/')
    def joined(message):
        cnt_to_mbti[session.get('cnt')] = session.get('userMBTI')
        room = session.get('room')
        join_room(room)
        if 'userID' in session:
            emit('status', {'msg': session.get('userNickname') + '님이 입장하셨습니다'}, room=room)
        else:
            emit('status', {'msg': '손님 [' + guest_number + ']님이 입장하셨습니다.'}, room=room)
    
    
    @socketio.on('text', namespace='/')
    def text(message):
        room = session.get('room')
        current_time = datetime.now().strftime('%p %I:%M')
        meridiem = current_time.split()[0]  # 오전 또는 오후
        if meridiem == 'AM':
            meridiem = '오전'
        else:
            meridiem = '오후'
        time = current_time.split()[1]  # 시간
        if 'userID' in session:
            message = '[' + session.get('userMBTI') + '] ' + session.get('userNickname') + '\n' + message['msg'] + ' (' + meridiem + ' ' + time + ')'
            emit('message', {'msg': message}, room=room)
        else:
            message = '손님 [' + guest_number + ']\n' + message['msg'] + ' (' + meridiem + ' ' + time + ')'
            emit('message', {'msg': message}, room=room)

    @socketio.on('left', namespace='/')
    def left(message):
        room = session.get('room')
        leave_room(room)
        emit('status', {'msg': session.get('name') + '님이 퇴장하셨습니다'}, room=room)