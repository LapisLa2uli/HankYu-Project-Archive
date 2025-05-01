import pyautogui, random
keys='abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
for i in range(random.randint(0,1000)):
    pyautogui.moveTo(x=random.randint(0,2000),y=random.randint(0,2000))
    pyautogui.keyDown(keys[random.randint(0,len(keys)-1)], logScreenshot=None, _pause=False)
    if random.randint(0,10)==1:
        pyautogui.alert(str="GIVE ME ALL YOUR MONEY OR I WILL BREAK oQzcvD9SybYOUR PC", title="YOU HAVE BEEN HACKED")