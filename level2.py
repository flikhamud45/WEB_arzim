import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return flask.render_template_string("hello world")

def main():
    app.run()

if __name__ == '__main__':
    main()