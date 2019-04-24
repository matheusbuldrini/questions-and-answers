from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import classes.user as User
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	perguntas = [{'id': 1, 'titulo': 'primeira perg', 'desc': 'bla bla bla'}, {'id': 2, 'titulo': 'segunda perg', 'desc': 'mais bla bla bla'}]
	return render_template('home.html', perguntas=perguntas)

@app.route("/pergunta/<int:pergunta_id>/")
def pergunta(pergunta_id):
    return render_template('pergunta.html',pergunta_id=pergunta_id)

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        user = User.User()
        return str(user.validate_register(request.form['fullname'], request.form['email'], request.form['password']))
    else:
        return render_template('cadastro.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.User()
        return str(user.validate_login(request.form['email'], request.form['password']))
    else:
        return render_template('login.html')

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
