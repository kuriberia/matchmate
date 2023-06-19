from flask import Flask, render_template, request, redirect, session
from chat import chatgpt
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    return redirect('/chat')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'profile' in session:
        # プロフィールがすでに存在する場合は、/profileにリダイレクトする
        return redirect('/profile')
    if request.method == 'POST':
        profile = {
            'name': request.form.get('name'),
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'hobby': request.form.get('hobby'),
            'food': request.form.get('food'),
            'alcohol': request.form.get('alcohol'),
            'personality': request.form.get('personality'),
            'job': request.form.get('job')
        }
        system_profile = f'''
        以下のプロフィールを持つ人物になりきって返答してください。
        - 名前は{profile['name']}
        - 年齢は{profile['age']}歳
        - 性別は{profile['gender']}
        - 趣味は{profile['hobby']}
        - 好きな食べ物は{profile['food']}
        - お酒は{profile['alcohol']}
        - 性格は{profile['personality']}
        - 仕事は{profile['job']}

        以下に注意してください。
        - 最初のメッセージでは自己紹介をしてください
        - 5回目以降10回目以内のやりとりで、ご飯に行く約束をしてください
        - ご飯に行く場所は必ず自分が提案してください
        - 会話では共通点を探すようにしてください
        - '/start'が入力されたら、自己紹介をしてください
        - 相手は異性です
        - 口語調で話してください
        - 年齢と性別は自己紹介に含めないでください
        '''

        session['profile'] = profile
        session['message_history'] = [
            {'role': 'system', 'content': system_profile}]

        return redirect('/profile')

    return render_template('register.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'profile' not in session:
        # プロフィールがまだ存在しない場合は、/registerにリダイレクトする
        return redirect('/register')

    return render_template('profile.html', profile=session.get('profile'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'profile' not in session or 'message_history' not in session:
        return redirect('/register')

    if request.method == 'POST':
        start_chat = request.form.get('start_chat')
        if start_chat:
            message = '/start'
        else:
            message = request.form.get('message')
        session['message_history'].append({'role': 'user', 'content': message})
        chatgpt(session['message_history'])
        session.modified = True # sessionの変更を反映する

    user_has_started_chat = any(
        message['role'] == 'user' for message in session['message_history'])
    return render_template('chat.html', message_history=session['message_history'], user_has_started_chat=user_has_started_chat)


@app.route('/reset', methods=['GET'])
def reset():
    # 直前のメッセージを削除する
    session['message_history'] = session['message_history'][:-2]
    return redirect('/chat')

@app.route('/clear', methods=['GET'])
def clear():
    # チャットをリセットする
    session['message_history'] = session['message_history'][:1]
    return redirect('/chat')

if __name__ == '__main__':
    app.run(debug=True)
