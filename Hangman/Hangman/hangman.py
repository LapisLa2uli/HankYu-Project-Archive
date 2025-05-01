import random

def process(ans, gList, cnt):
    print(' '.join(gList))
    guess = input('Guess Letter/word: ')
    cnt += 1
    if len(guess) == len(ans):
        if guess == ans:
            for i in range(len(ans)):
                gList[i] = ans[i]
    elif len(guess) == 1:
        if not guess.isalpha():
            print("Input Error! Enter a character/Word with answer length!")
        else:
            guess = guess.lower()
            if guess in ans:
                for i in range(len(ans)):
                    if ans[i] == guess:
                        gList[i] = ans[i]
    else:
        print("Input Error! Enter a character/Word with answer length!")
    return gList, cnt



# ----- main -----
wfile = open("word_cloud.txt", "r")
wList = wfile.readlines()
while True:
    ans = random.choice(wList).rstrip('\n')
    ans = ans.lower()
    wLen = len(ans)
    gList = ['-'] * wLen
    cnt = 0
    while ''.join(gList) != ans:
        gList, cnt = process(ans, gList, cnt)
    print(f"Great! You solved it in {cnt} guesses!")
    print(ans)
    yn = input("Continue? (y/n)")
    if yn == 'n' or yn == 'N':
        break
wfile.close()


