from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from AnaDB import AnaDatabase
import random

app = Flask(__name__)
darkpaste = AnaDatabase("Darkpaste")

#darkpaste.create("users", ["user", "pass", "token", "ip"])
#darkpaste.create("pastes", ["url", "name", "content", "number", "poster", "private"])

darkpaste.load()

def getUser():
 token = request.cookies.get('token')
 ip = request.cookies.get('ip')
 if token == None: return False
 if ip == None: return False
 result = darkpaste.getWhere("users", "token=" + token, "select=ip")
 if len(result) == 0: return False
 if result[0][0] == ip:
  result = darkpaste.getWhere("users", "token=" + token, "select=user")   
  return result[0][0]
 return False

def checkLogged():
 token = request.cookies.get('token')
 ip = request.cookies.get('ip')
 if token == None: return False
 if ip == None: return False
 result = darkpaste.getWhere("users", "token=" + token, "select=ip")
 if len(result) == 0: return False
 if result[0][0] == ip: return True
 return False

def verifyLogin(username, password):
 global darkpaste
 result = darkpaste.getWhere("users", "user=" + username, "select=pass")
 if len(result) == 0: return False
 if result[0][0] == password: return True

@app.route('/handle_login', methods=['POST'])
def handle_login():
    global darkpaste
    username, password = request.values.get('user'), request.values.get('pass') 
    if verifyLogin(username, password): 
     resp = make_response(render_template('success.html'))
     token = generateUrl()
     ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
     resp.set_cookie('token', token)
     resp.set_cookie('ip', ip)
     darkpaste.update("users", "user=" + username, "token,ip", token, ip)
     return resp         
    return render_template('login.html')

def generateUrl():
 chars = "ABCDEFGHIJKLMNOPQRSTUVXYZabcdefhijklmnopqrstuvxyz1234567890"
 url = ""
 for x in range(0, 10):
  url += (random.choice(chars))
 return url

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/pastes/<url>")
def paste(url):
    global darkpaste
    content = (darkpaste.getWhere("pastes", "url=" + url, "select=name,content"))
    return render_template("paste/paste.html", content=content)

@app.route("/user/<url>")
def user(url):
    global darkpaste
    urls = (darkpaste.getWhere("pastes", "poster=" + url, "select=url"))
    titles = (darkpaste.getWhere("pastes", "poster=" + url, "select=name"))
    posters = (darkpaste.getWhere("pastes", "poster=" + url, "select=poster"))
    if len(urls) < 11: length = len(urls)
    else: length = 11
    return render_template('user/user.html', titles=titles, urls=urls, length=length, posters=posters)

@app.route("/")
def index():
    global darkpaste
    username = ""
    if checkLogged(): username = getUser()   
    urls = (darkpaste.getWhere("pastes", "number=0", "select=url"))
    titles = (darkpaste.getWhere("pastes", "number=0", "select=name"))
    posters = (darkpaste.getWhere("pastes", "number=0", "select=poster"))
    if len(urls) < 11: length = len(urls)
    else: length = 11
    return render_template('main.html', titles=titles, urls=urls, length=length, posters=posters, username=username)

@app.route("/paste")
def pastePage():
    if not checkLogged(): return render_template('notlogged.html')
    return render_template('paste.html')

@app.route('/create_paste', methods=['POST'])
def create_paste():
    if not checkLogged(): return render_template('notlogged.html')
    username = getUser()
    title, content = request.values.get('title'), request.values.get('content') 
    darkpaste.enter("pastes", [generateUrl(), title, content, 0, username, "false"])
    darkpaste.save()
    index()
    return index()

if __name__ == "__main__":
    app.run(debug=True)
