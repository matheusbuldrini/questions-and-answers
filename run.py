from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import classes.user as User
import classes.answer as Answer
import classes.question as Question

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route("/")
@app.route("/home")
def home():
    question = Question.Question()
    perguntas = question.get_all()
    return render_template('home.html', perguntas=perguntas)

@app.route('/login/unsuccessful')
def login_popup():
    return render_template('popup.html')

@app.route("/pergunta/<int:pergunta_id>/", methods=['GET', 'POST'])
def pergunta(pergunta_id):
    question = Question.Question()
    pergunta = question.get_by_id(str(pergunta_id))[0]
    pergunta_title = str(pergunta['title'])
    pergunta_desc = str(pergunta['description'])
    if request.method == 'POST':
        answer = Answer.Answer()
        respostas = answer._select_all_by_questionid(str(pergunta_id))
        answer_form = request.form['resposta']
        try:
            if session['logged_user_id']:
                answer._insert(str(pergunta_id), session.get('logged_user_id'), answer_form)
                answer_form = None
                return redirect(url_for('pergunta', pergunta_id=pergunta_id))
        except Exception:
            return redirect(url_for('login_popup'))
    else:
        answer = Answer.Answer()
        print(pergunta_title)
        respostas = answer._select_all_by_questionid(str(pergunta_id))
        return render_template('pergunta.html', pergunta_id=pergunta_id,
                               respostas=respostas,
                               pergunta_title=pergunta_title,
                               pergunta_desc=pergunta_desc)

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        user = User.User()
        if user.validate_register(request.form['fullname'], request.form['email'], request.form['password']):
            session['logged_user_id'] = user._select_id_by_email(request.form['email'])
            session['name'] = user.get_by_id(str(session['logged_user_id']))['fullname']
            return redirect(url_for('minha-conta.html'))
        else:
            return render_template('cadastro.html')
    else:
        return render_template('cadastro.html')

@app.route("/fazer-pergunta", methods=['GET', 'POST'])
def fazer_pergunta():
    if not session.get('logged_user_id'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            question = Question.Question()
            if question.validate_question_post(request.form['title'], request.form['body'], session.get('logged_user_id')):
                return redirect(url_for('minhas_perguntas'))
            else:
                render_template('popup.html', msg="Erro ao cadastrar pergunta", retry_url='/fazer-pergunta')
        else:
            return render_template('fazer-pergunta.html')

@app.route("/minha-conta")
def minha_conta():
    if request.method == 'POST':
        pass #atualiza os dados do usuario. Se a senha for != '', altera a senha também
    else:
        if session.get('logged_user_id'):
            user = User.User()
            data = user.get_by_id(str(session.get('logged_user_id')))
            if data:
                return render_template('minha-conta.html', user = data)
        return redirect(url_for('login'))

@app.route("/minhas-perguntas")
def minhas_perguntas():
    return "Minhas perguntas"

@app.route("/minhas-respostas")
def minhas_respostas():
    return "Minhas respostas"

@app.route("/remover-conta")
def remover_conta():
    return "Remover Conta"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.User()
        if user.validate_login(request.form['email'], request.form['password']):
            session['logged_user_id'] = user._select_id_by_email(request.form['email'])
            session['name'] = user.get_by_id(str(session['logged_user_id']))['fullname']
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login_popup'))
    else:
        return render_template('login.html')

@app.route("/sair")
def sair():
    # remove the username from the session if it is there
    session.pop('logged_user_id', None)
    session['name'] = ''
    return redirect(url_for('home'))

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
