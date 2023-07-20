# Chatting with unknown someone Sharing your MBTI automatically
# Find Look-Alike Celebrity (using CNN)

## 웹 사이트의 기능
### 메인 페이지 (index.html)
![1](https://github.com/ndb796/React-Multi-Page-Web-Template-1/assets/129146537/2b98807c-a2d0-4f3c-9072-7a1d90a0ec81)


### 회원가입 (join.html)
![image](https://github.com/ndb796/React-Multi-Page-Web-Template-1/assets/129146537/e4bb893f-81bd-4082-93af-62417a007bc3)
```html
<script>
  function check_ID_duplicate() {
    var userID = $('#userID').val();
    $.ajax({
      url: '/check_ID_duplicate',
      method: 'POST',
      data: { userID: userID },
      success: function(response) {
        if (response.duplicate) {
          alert('중복된 ID입니다.');
        } else {
          alert(userID + '은 사용 가능한 아이디입니다.');
          document.getElementById("joinForm").submit();
        }
      },
      error: function() {
        alert('ID 중복체크에 실패했습니다.');
      }
    });
  }
</script>
```
회원가입 시 중복 ID 확인 버튼을 눌렀을 때, ajax를 이용하여 비동기식으로 확인 가능하도록 하였다.

### 1:1 랜덤채팅 (chat_random.html)
![image](https://github.com/ndb796/React-Multi-Page-Web-Template-1/assets/129146537/1053d076-8e32-4cfb-8b6d-d153d195f102)
들어온 순서대로 2명씩 매칭되어 채팅할 수 있다. 이 때, 회원가입한 MBTI가 닉네임 옆에 표시되도록 하였다.

```python
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
    return render_template('chat_lobby.html')
```
chat_lobby.html 에서 입장하기 버튼을 누르면 chat_random.html로 이동하여 채팅하는 구조이다.  
route.py에서 먼저 전역변수로 카운트변수 cnt를 선언했다.  


그 뒤, method가 POST방식으로 chat_lobby.html에 접속했을 경우 ( 즉, chat_lobby.html에서 입장하기 버튼을 누른 경우 )
- cnt가 짝수라면 -> cnt 값의 room을 해당 클라이언트 세션에 할당하고 cnt를 1 증가시킨다.
- cnt가 홀수라면 -> cnt - 1 값의 room을 해당 클라이언트 세션에 할당하고 cnt를 1 증가시킨다..
이후에 같은 room 세션값을 가진 유저끼리 소켓으로 연결하였다. (chat.py)



### 닮은꼴 연예인 찾기
![image](https://github.com/ndb796/React-Multi-Page-Web-Template-1/assets/129146537/b27a776f-ecc1-4639-b995-5d8340000f32)
본인은 시간, 용량적 한계로 9명의 연예인에 대해서만 학습시켰다.

- 먼저 crawling.py에서 연예인 얼굴의 dataset을 수집한다.
이후 train.py에서 학습을 진행하고 저장된 model_weights.pth 가중치 파일을
route.py의 resemble 함수에서 활용하여 form 으로 받은 이미지와 닮은 연예인들을 찾아준다.
9명에 대해 각각 180개의 학습 사진 데이터, epoch = 50, batch_size = 10 으로 학습시켰다.
