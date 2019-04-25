from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, array
import os
import classes.user as User
import classes.answer as Answer


app = Flask(__name__)
app.secret_key = 'any random string'

@app.route("/")
@app.route("/home")
def home():
    perguntas = [{'id': 1, 'titulo': 'primeira perg', 'desc': 'bla bla bla'}, {'id': 2, 'titulo': 'segunda perg', 'desc': 'mais bla bla bla'}]

    return render_template('home.html', perguntas=perguntas)

@app.route('/login/unsuccessful')
def login_popup():
    return render_template('popup.html')

@app.route("/pergunta/<int:pergunta_id>/", methods=['GET', 'POST'])
def pergunta(pergunta_id):
    if request.method == 'POST':
        answer = Answer.Answer()
        pass
        # return str(answer._insert(pergunta_id, "1", request.form['resposta']))
    else:
        answer = Answer.Answer()
        respostas = answer._select_all_by_questionid(str(pergunta_id))
        return render_template('pergunta.html', pergunta_id=pergunta_id,
                               respostas=respostas)

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        user = User.User()
        if user.validate_register(request.form['fullname'], request.form['email'], request.form['password']):
            session['logged_user_id'] = user._select_id_by_email(request.form['email'])
            return render_template('minha-conta.html')
        else:
            return render_template('cadastro.html')
    else:
        return render_template('cadastro.html')

@app.route("/fazer-pergunta", methods=['GET', 'POST'])
def fazer_pergunta():
    if request.method == 'POST':
        # question = Question.Question()
        return str(question.validate_question_post(request.form['title'], request.form['body']))
    else:
        return render_template('fazer-pergunta.html')

@app.route("/minha-conta")
def minha_conta():
    if not session.get('logged_user_id'):
        return render_template('login.html')
    else:
        user = User.User()
        data = user._select_all_by_userid(session.get('logged_user_id'))
        return render_template('minha-conta.html', data = data)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.User()
        if user.validate_login(request.form['email'], request.form['password']):
            session['logged_user_id'] = user._select_id_by_email(request.form['email'])
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login_popup'))
            # return "Erro ao logar"
    else:
        return render_template('login.html')

@app.route("/sair")
def sair():
    # remove the username from the session if it is there
    session.pop('logged_user_id', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
