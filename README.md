# Darkpaste
<h3>Darkpaste is a simple Pastebin alternative made for private use by me and my friends. It is not intended to be deployed for anything but small scale use.</h3>

Darkpaste is made using [Flask](https://github.com/pallets/flask) & [AnaDB](https://github.com/10xJSChad/AnaDB) for login/paste storage. Login information is stored locally & is md5 hashed and salted, this is not very secure but it's better than nothing. The salt can be found & modified in Config.py

<h2>Features</h2>

* Post public, unlisted, or private pastes.
* Edit or delete pastes at any time
* Hashed & salted password storage
* Basic profile pages
* Very simple setup

The registration page can be enabled or disabled in Config.py <br>
Make accounts with User Creation.py if registration is disabled.

<h2>Requirements</h2>

* Flask

<h2>Examples</h2>

<img src="https://i.imgur.com/0ZFI3yH.png)" width="55%" height="85%"/>
<img src="https://i.imgur.com/zLSJMFM.png" width="55%" height="85%"/>
<img src="https://i.imgur.com/0O7FAJy.png" width="55%" height="85%"/>
