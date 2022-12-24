from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Go to /puppy_name/name and see"

@app.route('/information')
def info():
    return "<h1>Puppies are cute</h1>"

@app.route('/puppy_name/<name>')
def puppylatin(name):
    pupname = ''

    if name[-1] == 'y':
        pupname = name[:-1] + 'iful'
    else: 
        pupname = name + 'y'
    return "<h1>Your puppy name is {}".format(pupname) + "</h1>"

if __name__ == '__main__':
    app.run(debug=True)
