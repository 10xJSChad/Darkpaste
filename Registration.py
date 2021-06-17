from AnaDB import AnaDatabase
import hashlib
import Config

darkpaste = AnaDatabase("Darkpaste")

def hash(password):
    #This is very weak and should be re-written if you intend to use Darkpaste.
    result = hashlib.md5(password.encode())
    result = result.hexdigest()
    result += Config.passwordSalt;
    result = hashlib.md5(result.encode())
    return(result.hexdigest())

def register(username, password):
    global darkpaste
    darkpaste.load()
    result = (darkpaste.getWhere("users", "user=" + username.lower()))
    
    if result != []: return(False, "Username already taken")
    if len(password) < 3: return(False, "Password is too short")
    darkpaste.enter("users", [username.lower(), hash(password), "x", "x"])
    darkpaste.save()
    return(True, "Great success!")