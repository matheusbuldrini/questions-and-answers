# -*- coding: utf-8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

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

@app.route('/popup')
def popup(msg="Erro", links=[{'url': '/home', 'text': 'Home'}]):
    return render_template('popup.html', msg=msg, links=links)

@app.route("/pergunta/<int:pergunta_id>/", methods=['GET', 'POST'])
def pergunta(pergunta_id):
    question = Question.Question()
    pergunta = question.get_by_id(str(pergunta_id))[0]
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
            return popup()
    else:
        answer = Answer.Answer()
        respostas = answer._select_all_by_questionid(str(pergunta_id))
        return render_template('pergunta.html', pergunta_id=pergunta_id,
                               respostas = respostas,
                               pergunta_fullname = str(pergunta['fullname']),
                               pergunta_title = str(pergunta['title']),
                               pergunta_data = str(pergunta['data']),
                               pergunta_desc = str(pergunta['description']))

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        user = User.User()
        if user.validate_register(request.form['fullname'], request.form['email'], request.form['password']):
            session['logged_user_id'] = user._select_id_by_email(request.form['email'])
            session['name'] = user.get_by_id(str(session['logged_user_id']))['fullname']
            return redirect(url_for('minha_conta'))
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
                return redirect(url_for('home'))
            else:
                return popup(msg="Erro ao cadastrar pergunta", links=[{'url': '/fazer-pergunta', 'text': 'Tentar Novamente'}])
        else:
            return render_template('fazer-pergunta.html')

@app.route("/minha-conta", methods=['GET', 'POST'])
def minha_conta():
    if request.method == 'POST':
        user = User.User()
        if user.validate_update(request.form['fullname'], request.form['email'], request.form['password'], request.form['description'], str(session.get('logged_user_id'))):
            session['name'] = request.form['fullname']
            return redirect(url_for('minha_conta'))
        else:
            return popup(msg="Erro ao atualizar dados", links=[{'url': '/minha-conta', 'text': 'Tentar Novamente'}])
    else:
        if session.get('logged_user_id'):
            user = User.User()
            data = user.get_by_id(str(session.get('logged_user_id')))
            if data:
                return render_template('minha-conta.html', user = data)
        return redirect(url_for('login'))
    return redirect(url_for('minha_conta'))

@app.route("/minhas-perguntas")
def minhas_perguntas():
    if not session.get('logged_user_id'):
        return render_template('login.html')
    else:
        question = Question.Question()
        perguntas = question.get_by_user(str(session.get('logged_user_id')))
        return render_template('minhas-perguntas.html', perguntas=perguntas)

@app.route("/minhas-respostas")
def minhas_respostas():
    if not session.get('logged_user_id'):
        return render_template('login.html')
    else:
        answer = Answer.Answer()
        respostas = answer.get_by_user(str(session.get('logged_user_id')))
        return render_template('minhas-respostas.html', respostas=respostas)

@app.route("/remover-conta-confirmado")
def remover_conta_confirmado():
    if not session.get('logged_user_id'):
        return render_template('login.html')
    else:
        User.User()._delete(str(session.get('logged_user_id')))
        sair()
    return redirect(url_for('home'))

@app.route("/remover-conta")
def remover_conta():
    return popup(msg="Tem certeza que quer remover a sua conta?", links=[{'url': '/remover-conta-confirmado', 'text': 'Remover conta!!!'}, {'url': '/minha-conta', 'text': 'Voltar'}])

@app.route("/remover-pergunta/<int:pergunta_id>/", methods=['GET', 'POST'])
def remover_pergunta(pergunta_id):
    return popup(msg="Tem certeza que quer remover a sua pergunta?", links=[{'url': '/remover-pergunta-confirmado/' + str(pergunta_id), 'text': 'Remover pergunta!!!'}, {'url': '/minhas-perguntas', 'text': 'Voltar'}])

@app.route("/remover-pergunta-confirmado/<int:pergunta_id>/", methods=['GET', 'POST'])
def remover_pergunta_confirmado(pergunta_id):
    if not session.get('logged_user_id'):
        return render_template('login.html')
    else:
        Question.Question().remove(pergunta_id, str(session.get('logged_user_id')))
    return redirect(url_for('minhas_perguntas'))

@app.route("/pesquisar", methods=['POST'])
def pesquisar():
    if request.method == 'POST':
        question = Question.Question()
        perguntas = question.get_by_title(request.form['pesquisa'])
        return render_template('pesquisa.html', perguntas=perguntas)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.User()
        if user.validate_login(request.form['email'], request.form['password']):
            session['logged_user_id'] = user._select_id_by_email(request.form['email'])
            session['name'] = user.get_by_id(str(session['logged_user_id']))['fullname']
            return redirect(url_for('home'))
        else:
            return popup(msg="Erro ao fazer login", links=[{'url': '/login', 'text': 'Tentar Novamente'}])
    else:
        return render_template('login.html')

@app.route("/sair")
def sair():
    # remove the username from the session if it is there
    session.pop('logged_user_id', None)
    session.pop('name', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
