from flask import Flask, flash, redirect, render_template, request, session, abort
import os
app = Flask(__name__)

@app.route("/")
def index():
    return "Index!"

@app.route("/hello/<string:name>/")
def hello(name):
    return render_template('test.html',name=name)

@app.route("/members")
def members():
    return "Members"

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)