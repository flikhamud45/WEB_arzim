import flask
from flask import Flask

app = Flask(__name__)
app.template_folder = "."

@app.route('/')
def hello():
    name = flask.request.args.get("name", "")
    return flask.render_template("index.html", name=name)

def main():
    app.run()

if __name__ == '__main__':
    main()