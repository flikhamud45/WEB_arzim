import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    name = flask.request.args.get("name", "")
    return f"hello {name}"

def main():
    app.run()

if __name__ == '__main__':
    main()