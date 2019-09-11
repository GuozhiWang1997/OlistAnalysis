from flask import Flask
from dbutil import DB


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test')
def test():
    db = DB()
    data = db.executeSingleResult("SELECT COUNT(*) FROM CUSTOMER")
    db.close()
    return str(data)


if __name__ == '__main__':
    app.run()