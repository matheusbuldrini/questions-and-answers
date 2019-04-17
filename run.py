from flask import Flask, flash, redirect, render_template, request, session, abort
import os
app = Flask(__name__)

@app.route("/")	
@app.route("/home")
def home():
	perguntas = [{'id': 1, 'titulo': 'primeira perg', 'desc': 'bla bla bla'}, {'id': 2, 'titulo': 'segunda perg', 'desc': 'mais bla bla bla'}]
	return render_template('home.html', perguntas=perguntas)

@app.route("/pergunta/<string:pergunta_id>/")
def hello(pergunta_id):
    return render_template('pergunta.html',pergunta_id=pergunta_id)
	

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
