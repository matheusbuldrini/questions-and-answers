# -*- coding: utf-8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import json
import classes.user as User
import classes.answer as Answer
import classes.question as Question
import classes.votequestion as VoteQuestion
import classes.voteanswer as VoteAnswer
import classes.utils as Utils

app = Flask(__name__)
@app.context_processor
def inject_alert():
    return dict(get_alert=Utils.Utils().get_alert, unset_alert=Utils.Utils().unset_alert)

app.secret_key = 'any random string'

utils = Utils.Utils()

@app.route("/")
@app.route("/home")
def home():
    question = Question.Question()
    perguntas = question.get_all()
    # perguntas = [{'idquestion': 1, 'title': 'Why?', 'description': 'hihi', 'data': '2017',
    #               'fullname': 'Effy', 'tags': ['linux', 'arch']}]
    return render_template('home.html', perguntas=perguntas)

@app.route('/popup')
def popup(msg="Erro", links=[{'url': '/home', 'text': 'Home'}]):
    return render_template('popup.html', msg=msg, links=links)

@app.route("/pergunta/<int:pergunta_id>/", methods=['GET', 'POST'])
def pergunta(pergunta_id):
    question = Question.Question()
    pergunta = question.get_by_id(str(pergunta_id))
    if request.method == 'POST':
        answer = Answer.Answer()
        if session['logged_user_id']:
            if answer.validate_answer_post(str(pergunta_id), session.get('logged_user_id'), request.form['resposta']):
                utils.set_alert('success', 'Resposta postada!')
                return redirect(url_for('pergunta', pergunta_id=pergunta_id))
        return popup(msg="Erro ao cadastrar resposta", links=[{'url': '/pergunta/' + str(pergunta_id), 'text': 'Voltar'}])
    else:
        answer = Answer.Answer()
        respostas = answer._select_all_by_questionid(str(pergunta_id))
        return render_template('pergunta.html', pergunta_id=pergunta_id,
                               respostas = respostas,
                               usuario_logado = session.get('logged_user_id'),
                               pergunta_votes = str(pergunta['votes']),
                               pergunta_fullname = str(pergunta['fullname']),
                               pergunta_title = str(pergunta['title']),
                               pergunta_data = str(pergunta['data']),
                               pergunta_desc = str(pergunta['description']))

@app.route("/pergunta-votar", methods=['POST'])
def votar_pergunta():
    if not session.get('logged_user_id'):
        return render_template('login.html')
    else:
        if request.method == "POST":
            question_id = request.json['id']
            question_vote = request.json['vote']
            votequestion = VoteQuestion.VoteQuestion()
            if votequestion.validate_vote(question_id, str(session.get('logged_user_id')), question_vote):
                return redirect(url_for('pergunta', pergunta_id=question_id))

@app.route("/resposta-votar", methods=['POST'])
def votar_resposta():
    if not session.get('logged_user_id'):
        return render_template('login.html')
    else:
        if request.method == "POST":
            question_id = request.json['idquestion']
            answer_id = request.json['idanswer']
            answer_vote = request.json['vote']
            voteanswer = VoteAnswer.VoteAnswer()
            if voteanswer.validate_vote(answer_id, str(session.get('logged_user_id')), answer_vote):
                return redirect(url_for('pergunta', pergunta_id=question_id))

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        user = User.User()
        if user.validate_register(request.form['fullname'], request.form['email'], request.form['password']):
            session['logged_user_id'] = user._select_id_by_email(request.form['email'])
            session['name'] = user.get_by_id(str(session['logged_user_id']))['fullname']
            utils.set_alert('success', 'Registrado!')
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
            tags = request.form['tag'].split(',')

            dict_tag = {'Tags': dict(('tag ' + str(i), item) for i, item in enumerate(tags))}
            dict_tag = json.dumps(dict_tag)

            if question.validate_question_post(request.form['title'], request.form['body'], session.get('logged_user_id'), dict_tag, False):
                utils.set_alert('success', 'Pergunta postada!')
                return redirect(url_for('home'))
            else:
                return popup(msg="Erro ao cadastrar pergunta", links=[{'url': '/fazer-pergunta', 'text': 'Tentar Novamente'}])
        else:
            return render_template('fazer-pergunta.html')


@app.route("/editar-pergunta/<int:pergunta_id>/", methods=['GET', 'POST'])
def editar_pergunta(pergunta_id):
    question = Question.Question()
    pergunta = question.get_by_id(str(pergunta_id))
    if request.method == 'POST':
        if question.validate_question_post(request.form['title'], request.form['description'], session.get('logged_user_id'), str(pergunta_id)):
            utils.set_alert('success', 'Pergunta editada!')
            return redirect(url_for('minhas_perguntas'))
        else:
            return popup(msg="Erro ao editar pergunta", links=[{'url': '/editar-pergunta/'+str(pergunta_id), 'text': 'Tentar Novamente'}])
    else:
        if(int((pergunta['iduser'])) == int(session['logged_user_id'])):
            return render_template('editar-pergunta.html', pergunta_id=pergunta_id,
                                   pergunta_title = str(pergunta['title']),
                                   pergunta_desc = str(pergunta['description']))
        else:
            return redirect(url_for('home'))

@app.route("/editar-resposta/<int:resposta_id>/", methods=['GET', 'POST'])
def editar_resposta(resposta_id):
    answer = Answer.Answer()
    resposta = answer.get_by_id(str(resposta_id))
    if request.method == 'POST':
        if answer.validate_answer_edit(request.form['description'], session.get('logged_user_id'), str(resposta_id)):
            utils.set_alert('success', 'Resposta editada!')
            return redirect(url_for('minhas_respostas'))
        else:
            return popup(msg="Erro ao editar resposta", links=[{'url': '/editar-resposta/'+str(resposta_id), 'text': 'Tentar Novamente'}])
    else:
        if(int((resposta['iduser'])) == int(session['logged_user_id'])):
            return render_template('editar-resposta.html', resposta_id=resposta_id,
                                   pergunta_title = str(resposta['title']),
                                   resposta_desc = str(resposta['description']))
        else:
            return redirect(url_for('home'))


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
        utils.set_alert('success', 'Pergunta removida!')
    return redirect(url_for('minhas_perguntas'))


@app.route("/remover-resposta/<int:resposta_id>/", methods=['GET', 'POST'])
def remover_resposta(resposta_id):
    return popup(msg="Tem certeza que quer remover a sua resposta?", links=[{'url': '/remover-resposta-confirmado/' + str(resposta_id), 'text': 'Remover resposta!!!'}, {'url': '/minhas-respostas', 'text': 'Voltar'}])

@app.route("/remover-resposta-confirmado/<int:resposta_id>/", methods=['GET', 'POST'])
def remover_resposta_confirmado(resposta_id):
    if not session.get('logged_user_id'):
        return render_template('login.html')
    else:
        Answer.Answer().remove(resposta_id, str(session.get('logged_user_id')))
        utils.set_alert('success', 'Resposta removida!')
    return redirect(url_for('minhas_respostas'))


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
