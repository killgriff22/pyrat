import flask,requests,threading
from flask import Flask
serv = Flask("client2")
active = True
def flaskthread():
    serv.run("0.0.0.0",42012)
def requestthread():
    global active
    import requests
    print("searching for client1, this thread will hang when found")
    while active:
        try:
            r = requests.post("http://localhost:42011/link")
        except:
            class r:
                text = ""
        if r.text == "DISCONNECT":
            active = False
@serv.route("/link", methods=["POST"])
def link():
    #this will hang, make sure this is running in a thread
    while active:
        pass
    return "DISCONNECT"
fthread = threading.Thread(target=flaskthread)
rthread = threading.Thread(target=requestthread)
fthread.start()
rthread.start()