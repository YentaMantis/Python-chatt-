import sqlite3
from flask import Flask, render_template, url_for, request, session, redirect, make_response, session, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
import datetime
import os
import contextlib

FC = True
NULL = 0

USERNAME = 0


# class instances
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.urandom(24)


app.secret_key = 'my-seCret_KEy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatt.db'
socketio = SocketIO(app, cors_allowed_origins='*', engineio_logger=True)
#engine
#engine = create_engine("sqlite:///chatt.db")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                # integral för att holla koll på medelanden
    message = db.Column(db.String(200), nullable=False)                         # message, kollumn med typen "db.string", längd 200. kan inte ha ett värde av NULL (0, eller ingenting)
    user = db.Column(db.String(200), nullable=False)                            # user, kollumn med typen "db.string", längd 200. kan inte ha ett värde av NULL (0, eller ingenting)     (db är instans av klassen "SQLAlchemy")
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)     # date_created, kollumn med typen "db.datetim", längd 200. kan inte ha ett värde av NULL (0, eller ingenting)

    def __repr__(self):
        return "<message: %r>" % self.id
    
@app.route("/", methods=["POST", "GET"])
def index():
    session['username'] = 0
    a = 0
    global NAME
    if request.method == 'POST':
        session['username'] = request.form['name']
        return redirect("/chatt")
    else:
        return render_template("index.html")
@app.route("/delete/<int:id>")
def delete(id):
    delete = User.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
    except:
        return render_template("index.html")


@app.route("/chatt/")
def GetUsrName():
    global USERNAME
    a = session["username"]
    USERNAME = a
    return render_template("chatt.html", messages=User.query.order_by(User.date_created).all())

@socketio.on('message')
def handleMessage(msg):
    global FC
    global USERNAME
    global session
    if session['username'] != 0:
        msg = session['username']+" >> "+msg
    else:
        msg = "anonymos: "



    send(msg, broadcast=True)
    bulk = User(user="testUsr", message=msg)
    try:
        db.session.add(bulk)                
        db.session.commit()
    except:
        return render_template("error.html")

@app.route("/delHist")
def ClearDataBase():
        #engine.execute("'DELETE FROM message'")
        return redirect("/")

@app.route("/secret")
def DisplayChattAnyway():
        return render_template("chatt.html", messages=User.query.order_by(User.date_created).all())


if __name__ == '__main__':
    socketio.run(app)
# Sqlite documentation: https://add0n.com/sqlite-manager.html?version=0.4.3&type=install
# Sqlite edeting online: https://sqliteonline.com/