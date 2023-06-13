import hashlib
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

def check_exist_for_signin(mail) -> bool:
    data = get_from_database(f"SELECT mail from users where mail = '{mail}'")
    return True if data else False

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


def check_user_for_login(mail, password) -> bool:
    data = get_from_database(f"SELECT mail, password from users where mail = '{mail}' AND password = '{hashlib.sha256(password.encode()).hexdigest()}'")
    return True if data else False


def create_user(mail, password, first_name, last_name):
    get_from_database(f"INSERT INTO users VALUES ('{mail}', '{hashlib.sha256(password.encode()).hexdigest()}', '{first_name}', '{last_name}')")

def get_name(mail) -> list:
    data = get_from_database(f"SELECT mail, password, first_name, last_name from users where mail = '{mail}'")
    return data[0][2:4]

@app.route('/', methods = ['GET', 'POST'])
def hello():
    if flask.request.method == "GET":
        return flask.render_template("index.html", tab=flask.request.args.get("tab"))
    elif flask.request.method == "POST":
        data = flask.request.form
        print(data)
        if "login_mail" in data:
            if check_user_for_login(data["login_mail"], data["password"]):
                resp = flask.make_response(flask.redirect("mainPage"))
                resp.set_cookie("mail", data["login_mail"])
                resp.set_cookie("pass", data["password"])
                return resp
            else:
                return "WRONG!!!!!"
        if check_exist_for_signin(data["mail"]):
            return "mail already exist"
        else:
            create_user(data["mail"], data["password"], data["first_name"], data["last_name"])
            return flask.redirect("/?tab=login")

    return "WHAT???"

@app.route('/mainPage')
def main_page():
    mail = flask.request.cookies.get("mail")
    password = flask.request.cookies.get("pass")
    if check_user_for_login(mail, password):
        return flask.render_template("connected.html", name=" ".join(get_name(mail)))
    else:
        return "Dont תעצבן אותי"

def main():
    t = threading.Thread(target=database_handler)
    t.start()
    app.run()


if __name__ == '__main__':
    main()