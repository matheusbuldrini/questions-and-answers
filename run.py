from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import classes.Database as Database
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
        return str(request.form)
    else:
        return render_template('cadastro.html')

@app.route("/testdb/")
def testdb():
	db = Database.Database()
	#return str(db.list("SELECT nickname, password FROM user"))
	return str(db.sql('UPDATE user SET password="827CCB0EEA8A706C4C34A16891F84E7J"'))
	#return str(db.list('INSERT INTO user VALUES (NULL, "test", "827CCB0EEA8A706C4C34A16891F84E7B")'))
    #return render_template('usuario.html',usuario_id=usuario_id)

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
