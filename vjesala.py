from flask import Flask
from flask import render_template
from flask import request
import random
import requests

def get_word():
    api_url = 'https://random-word-api.herokuapp.com/word'
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        print("nova rijec:", response.text)
        return response.text
    else:
        print("Error:", response.status_code, response.text)
        return "error"


app = Flask(__name__)
rijeci = [get_word()]
rijec_index = 0
slova = set(" ")
zivoti = 10


@app.route("/")
def hello_world():
    #return "<p>Dobro dosli u vjesala!</p>"
    return render_template('index.html')

@app.route("/nova-igra", methods=['GET', 'POST'])
def nova_igra():
    global slova, rijeci, zivoti, rijec_index
    d = None
    if request.method == "GET":
        slova = set(" ")
        rijeci = [get_word().lower()]
        rijec_index = random.randint(0,len(rijeci)-1)
        zivoti = 10

    if request.method == 'POST' and request.form['slovo']:
        d = request.form['slovo'].lower()
        slova.add(d[0])
    n = ""
    rijec = rijeci[rijec_index]
    rijec = rijec[2:-2]

    for a in rijec:
        if a.isspace() == True:
            n += "⨼ "
        elif a in slova:
            n += f"{a} "
        else:
            n += "_ "

    if d != None and d not in rijec:
        zivoti -= 1

    x = ", ".join(slova)
    pobjeda = "_" not in n

    return render_template("nova_igra.html", rijec=rijec, displej=n, z=zivoti, x=x, pobjeda=pobjeda)
