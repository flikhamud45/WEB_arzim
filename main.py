import sqlite3
import threading

import flask
from flask import Flask

app = Flask(__name__)
app.template_folder = "."
database_missions = {}
def get_from_database(mission):
    database_missions[threading.current_thread()] = mission
    while database_missions[threading.current_thread()] == mission:
        pass
    answer = database_missions[threading.current_thread()]
    del database_missions[threading.current_thread()]
    return answer

def database_handler():
    users_database = sqlite3.connect('database.db')
    cursur = users_database.cursor()
    try:
        while True:
            for key, mission in list(database_missions.items()):
                if type(mission) == str:
                    cursur.execute(mission)
                    database_missions[key] = cursur.fetchall()
                    users_database.commit()

    finally:
        cursur.close()
        users_database.close()
@app.route('/', methods = ['GET', 'POST'])
def hello():
    if flask.request.method == "GET":
        return flask.render_template("index.html")
    elif flask.request.method == "POST":
        data = flask.request.form
        print(data)
        return flask.redirect("/")
    return "WHAT???"

def main():
    app.run()

if __name__ == '__main__':
    main()