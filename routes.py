from flask import session, redirect, url_for, render_template, request, Blueprint, flash
from flask import Flask, jsonify, request, render_template, make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
import os
from flask_socketio import SocketIO, send
from model.user import User
from model.bbs import Bbs
import random
from PIL import Image
import torch
from train import *
import io
from torchvision import transforms

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    rand = str(random.randrange(1000,10000))
    if 'userID' in session:
        session['room'] = 'room'
        return render_template('index.html', userMBTI = session.get("userMBTI"), userNickname = session.get("userNickname"), room='room')
    else:
        session['room'] = 'room'
        return render_template('index.html', userMBTI = 'GUEST', userNickname = rand, room ='room')
    
@bp.route('/resemble', methods=['GET', 'POST'])
def resemble():
    if request.method == 'POST':
        if request.files['file'].filename == '':
            flash('이미지를 선택해 주세요.')
            return render_template("resemble.html")
        model = models.resnet34()
        model.fc = nn.Linear(model.fc.in_features, 9)
        model.load_state_dict(torch.load('model_weights.pth'))
        model = model.to(device)

        file = request.files['file']

        image = Image.open(io.BytesIO(file.read()))
        image = image.convert('RGB')
        image.save('image_save.jpg',"JPEG")
        image = Image.open('image_save.jpg')

        image = transforms_test(image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(image)
            
            _, preds = torch.max(outputs, 1)
            print(preds[0])
            imshow(image.cpu().data[0], title='예측 결과: ' + class_names[preds[0]])
        return redirect(request.referrer)
    return render_template('resemble.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'userID' in session:
        flash("이미 로그인되어 있습니다.")
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        userID = request.form['userID']
        userPassword = request.form['userPassword']
        user = User()
        result = user.login(userID, userPassword)
        if result == 1:
            flash("아이디를 입력해 주세요.")
            return render_template("login.html")
        elif result == 2:
            flash("비밀번호를 입력해 주세요.")
            return render_template("login.html")
        elif result == 3:
            flash("존재하지 않는 아이디입니다.")
            return render_template("login.html")
        elif result == 4:
            flash("비밀번호가 틀렸습니다.")
            return render_template("login.html")
        elif result == 5:
            flash("로그인에 실패했습니다.")
        else:
            return redirect(url_for('main.index'))
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.route('/join', methods=['GET', 'POST'])
def join():
    if 'userID' in session:
        flash("이미 로그인되어 있습니다.")
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        userID = request.form['userID']
        userPassword = request.form['userPassword']
        userName = request.form['userName']
        userNickname = request.form['userNickname']
        userEmail = request.form['userEmail']
        userGender = request.form['userGender']
        userMBTI = request.form['IE']+request.form['SN']+request.form['FT']+request.form['JP']
        user = User()
        result = user.join(userID, userPassword, userName, userNickname, userEmail, userGender, userMBTI)
        if result == 1:
            flash("아이디를 입력해 주세요.")
            return render_template("join.html")
        if result == 2:
            flash("중복된 아이디입니다.")
            return render_template("join.html")
        if result == 3:
            flash("ID는 영문 소문자, 숫자와 특수기호(_)만 사용 가능합니다.")
            return render_template("join.html")
        if result == 4:
            flash("비밀번호를 입력해 주세요.")
            return render_template("join.html")
        if result == 5:
            flash("이름을 입력해 주세요.")
            return render_template("join.html")
        if result == 6:
            flash("닉네임을 입력해 주세요.")
            return render_template("join.html")
        if result == 7:
            flash("성별을 선택해 주세요.")
            return render_template("join.html")
        else:
            flash("회원가입 완료. " + userID + "님 환영합니다.")
            return redirect(url_for('main.index'))
    return render_template('join.html')

cnt = 0
@bp.route('/chat_lobby', methods=['GET', 'POST'])
def chat_lobby():
    if request.method == 'POST':
        global cnt
        if cnt == 10000: # (10000 / 2) ==> 최대 5000개의 채팅방
            cnt -= 10000
        if cnt % 2 == 1:
            room = cnt - 1
        else:
            room = cnt
        session['cnt'] = cnt
        session['room'] = room
        cnt += 1
        if cnt % 2 == 1:
            session['waiting'] = 'True'
            return render_template('chat_random.html', waiting=True)
        else:
            session['waiting'] = 'Flase'
            return render_template('chat_random.html', waiting=False)
    return render_template('chat_lobby.html')

@bp.route('/chat_random')
def chat_random():
    if 'userID' not in session:
        flash("로그인 후 이용해 주세요.")
        return redirect(request.referrer)
    userNickname = session.get('userNickname')
    userMBTI = session.get('userMBTI')
    room = session.get('room')
    return render_template('chat_random.html', userNickname=userNickname, userMBTI=userMBTI, room=room)

@bp.route('/info')
def info():
    return render_template('info.html')

@bp.route('/bbs')
def bbs():
    bbs = Bbs()
    return render_template('bbs.html', bbsList = bbs.getList())

@bp.route('/bbs_write', methods=['GET', 'POST'])
def bbs_write():
    if 'userID' not in session:
        flash("로그인 후 이용해 주세요.")
        return redirect(request.referrer)
    if request.method == 'POST':
        bbsTitle = request.form['bbsTitle']
        bbsContent = request.form['bbsContent']
        if bbsTitle == '' or bbsContent == '':
            flash("입력이 안 된 사항이 있습니다.")
            return redirect(request.referrer)
        bbs = Bbs()
        bbs.write(bbsTitle, session.get('userNickname'), bbsContent)
        return redirect(url_for('main.bbs'))
    else:
        return render_template('bbs_write.html')

@bp.route('/bbs_view/<int:bbsID>')
def bbs_view(bbsID):
    bbs = Bbs()
    return render_template('bbs_view.html', board=bbs.getBoard(bbsID))

@bp.route('/check_ID_duplicate', methods=['POST'])
def check_ID_duplicate():
    userID = request.form['userID']
    user = User()
    duplicate = user.ID_duplicated(userID)
    if duplicate:
        response = {'duplicate': True}
    else:
        response = {'duplicate': False}
    return jsonify(response)