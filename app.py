from flask import Flask
import logging

app = Flask(__name__)

@app.route('/')
def welcome():
    return "hello world"

@app.route('/home')
def home():
    return "this is home page"

try:
    from controllers import *
except Exception as e:
    print(e)

if __name__ == '__main__':
    app.run(debug=True)
    logging.basicConfig(filename="app.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)