from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from AnaDB import AnaDatabase
import Registration
import Config
import random
import os

app = Flask(__name__)
darkpaste = AnaDatabase("Darkpaste")

#darkpaste.create("users", ["user", "pass", "token", "ip"])
#darkpaste.create("pastes", ["url", "name", "content", "number", "poster", "type"])
#darkpaste.save()

def resetDb():
 darkpaste.create("users", ["user", "pass", "token", "ip"])
 darkpaste.create("pastes", ["url", "name", "content", "number", "poster", "type"])
 darkpaste.save()
 exit()

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

def checkLoggedGetUser():
 token = request.cookies.get('token')
 ip = request.cookies.get('ip')
 if token == None: return False, "Guest"
 if ip == None: return False, "Guest"
 result = darkpaste.getWhere("users", "token=" + token, "select=user,ip")
 if len(result) == 0: return False, "Guest"
 if result[0][1] == ip: return True, result[0][0]
 return False, "Guest"

def verifyLogin(username, password):
 global darkpaste
 password = Registration.hash(password)
 result = darkpaste.getWhere("users", "user=" + username.lower(), "select=pass")
 if len(result) == 0: return False
 if result[0][0] == password: return True

@app.route('/handle_login', methods=['POST'])
def handle_login():
    global darkpaste
    username, password = request.values.get('user').lower(), request.values.get('pass') 
    if verifyLogin(username, password): 
     resp = make_response(render_template('success.html'))
     token = generateUrl()
     ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
     resp.set_cookie('token', token)
     resp.set_cookie('ip', ip)
     darkpaste.update("users", "user=" + username, "token,ip", token, ip)
     return resp         
    return render_template('login.html')

@app.route("/handle_registration", methods=['POST'])
def handle_registration():
    global darkpaste
    if Config.enableRegistration == False:
        return(index())
        
    username, password = request.values.get('user'), request.values.get('pass')
    result = Registration.register(username, password)
    if(result[0] == False): 
        return render_template('register.html', error=result[1])
    else: darkpaste.load(); return render_template('login.html');

@app.route("/edit/<url>")
def edit(url):
    global darkpaste
    viewingUser = checkLoggedGetUser()[1]
    isOwner = False
    
    content = (darkpaste.getWhere("pastes", "url=" + url, "select=name,content,poster,type,url"))
    privateContent = [["You do not own this paste", "Only the owner of this paste can edit it", content[0][2]]]
    if content[0][2] == viewingUser: isOwner = True
    
    if (isOwner == False):
     return render_template("paste/paste.html", content=privateContent)
 
    return render_template("editPaste.html", content=content)


@app.route("/delete/<url>")
def deletion(url):
    global darkpaste
    viewingUser = checkLoggedGetUser()[1]
    isOwner = False
    
    content = (darkpaste.getWhere("pastes", "url=" + url, "select=name,content,poster,type"))
    
    deleteContent = [["Paste Deleted", "Paste successfully deleted", content[0][2]]]
    privateContent = [["You do not own this paste", "Only the owner of this paste can delete it", content[0][2]]]
    
    if content[0][2] == viewingUser: isOwner = True
    
    if (isOwner == False):
     return render_template("paste/paste.html", content=privateContent)
 
    darkpaste.removeWhere("pastes", "url=" + url)
    darkpaste.save()
    return render_template("paste/paste.html", content=deleteContent)

def generateUrl():
 chars = "ABCDEFGHIJKLMNOPQRSTUVXYZabcdefhijklmnopqrstuvxyz1234567890"
 url = ""
 for x in range(0, 10):
  url += (random.choice(chars))
 return url

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    if Config.enableRegistration == False:
        return(index())
    return render_template('register.html')

@app.route("/pastes/<url>")
def paste(url):
    global darkpaste
    viewingUser = checkLoggedGetUser()[1]
    isOwner = False
    
    content = (darkpaste.getWhere("pastes", "url=" + url, "select=name,content,poster,type"))
    privateContent = [["Private Paste", "Only the owner of this paste can view it", content[0][2]]]
    if content[0][2] == viewingUser: isOwner = True
    
    if (content[0][3] == "private" and isOwner == False):
     return render_template("paste/paste.html", content=privateContent)
 
    return render_template("paste/paste.html", content=content)

@app.route("/user/<url>")
def user(url):
    global darkpaste
    viewingUser = checkLoggedGetUser()[1]
    urls = (darkpaste.getWhere("pastes", "poster=" + url, "select=url,type"))
    titles = (darkpaste.getWhere("pastes", "poster=" + url, "select=name,type"))
    posters = (darkpaste.getWhere("pastes", "poster=" + url, "select=poster,type"))
    isOwner = False
    
    newUrls = []
    newTitles = []
    newPosters = []

    if viewingUser != url:
     for x in urls: 
         if x[1] == "public": newUrls.append(x[0])   
     for x in titles: 
         if x[1] == "public": newTitles.append(x[0])       
     for x in posters: 
         if x[1] == "public": newPosters.append(x[0]) 
         
    else:
     isOwner = True
     for x in urls: 
         newUrls.append(x[0])   
     for x in titles: 
         newTitles.append(x[0] + " (" + x[1] + ")")
     for x in posters: 
         newPosters.append(x[0])
     
    urls = newUrls
    titles = newTitles
    posters = newPosters   
    
    length = len(urls)
    return render_template('user/user.html', titles=titles, urls=urls, length=length, posters=posters, isOwner=isOwner)

@app.route("/")
def index():
    global darkpaste
    username = ""
    if checkLogged(): username = getUser()   
    urls = (darkpaste.getWhere("pastes", "type=public", "select=url"))
    titles = (darkpaste.getWhere("pastes", "type=public", "select=name"))
    posters = (darkpaste.getWhere("pastes", "type=public", "select=poster"))
    if len(urls) < 11: length = len(urls)
    else: length = 11
    return render_template('main.html', titles=titles, urls=urls, length=length, posters=posters, username=username, loggedIn = checkLogged(), registrationEnabled = Config.enableRegistration)

@app.route("/paste")
def pastePage():
    if not checkLogged(): return render_template('notlogged.html', registrationEnabled = Config.enableRegistration)
    return render_template('paste.html')

@app.route('/update_paste', methods=['POST'])
def update_paste():
    username = getUser()
    title, content, pasteType, url = request.values.get('title'), request.values.get('content'), request.values.get('pasteType'), request.values.get('url')
    fixedPasteType = "public"
    
    loggedUser = checkLoggedGetUser()[1]
    pasteOwner = darkpaste.getWhere("pastes", "url=" + url, "select=poster")[0][0]
    
    if loggedUser != pasteOwner: return index()
        
    if pasteType == "public": fixedPasteType = pasteType
    if pasteType == "unlisted": fixedPasteType = pasteType
    if pasteType == "private": fixedPasteType = pasteType
    darkpaste.update("pastes", "url=" + url, "name,content,number,poster,type", title, content, 0, username, fixedPasteType)
    darkpaste.save()  
    
    return index()

@app.route('/create_paste', methods=['POST'])
def create_paste():
    if not checkLogged(): return render_template('notlogged.html')
    username = getUser()
    title, content, pasteType = request.values.get('title'), request.values.get('content'), request.values.get('pasteType')
    fixedPasteType = "public"
    
    if pasteType == "public": fixedPasteType = pasteType
    if pasteType == "unlisted": fixedPasteType = pasteType
    if pasteType == "private": fixedPasteType = pasteType
    
    darkpaste.enter("pastes", [generateUrl(), title, content, 0, username, fixedPasteType])
    darkpaste.save()
    index()
    return index()

if __name__ == "__main__":
    app.run()
