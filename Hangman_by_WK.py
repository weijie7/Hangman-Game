import pygame
import random
import math
import sys
import os
pygame.init()

size = width, height = 600, 500
screen = pygame.display.set_mode(size)

white = (255, 255, 255) 
green = (0, 255, 0) 
purple = (48, 43, 67)
tomato = (255,99,71)

######################
## Global Variables ##
######################
cdir = os.getcwd() + '\gallery\\'

font = pygame.font.Font(cdir+"AGENTORANGE.TTF", 65)
subtitlefont = pygame.font.Font(cdir+"AGENTORANGE.TTF", 25)
subfont = pygame.font.SysFont("comicsansms",17)
textfont = pygame.font.SysFont("comicsansms",30)

title = font.render("HANGMAN",True, white)
subtitle = subfont.render("created by wk", True, white)

hangmanpics = [pygame.image.load(cdir+'hangman0.png'), pygame.image.load(cdir+'hangman1.png'), pygame.image.load(cdir+'hangman2.png'), pygame.image.load(cdir+'hangman3.png'), pygame.image.load(cdir+'hangman4.png'),pygame.image.load(cdir+'hangman5.png')]

file = open(cdir+'words.txt',"r")
f = file.readlines()
file.close()

######################
## Screens          ##
######################

def homepage():
    screen.fill(purple)
    screen.blit(title, (size[0]/2-title.get_width()/2,20))
    screen.blit(subtitle,(size[0]/2+title.get_width()/2-subtitle.get_width(),title.get_height()+20))
    pygame.display.update()

def ingame():
    global textline, split, min_pos
    #each line 18 charc including space. Determine which space to split
    textline = math.ceil(len(display_word)/18)    
    if textline > 1:
        split = [pos for pos,char in enumerate(display_word) if char == " "]
        min_pos = [abs(i-18) for i in split].index(min([abs(i-18) for i in split]))
        for i in range(2):
            text = textfont.render(" ".join(display_word[i*split[min_pos]+i : split[min_pos]+i*split[min_pos]+1 ]), True, white)
            screen.blit(text, (50,175+i*65))
    else:
        text = textfont.render(" ".join(display_word), True, white)
        screen.blit(text, (50,175))
    
    msg_txt = subfont.render(msg, True, green)
    screen.blit(msg_txt, (size[0]/2+msg_txt.get_width()/2-msg_txt.get_width(),140))
    
    img = hangmanpics[5- lifecount]
    screen.blit(img, (400,size[1] - img.get_height()-20))
    
    wrong_guess_title = subtitlefont.render("Wrong Guess!", True, white)
    screen.blit(wrong_guess_title, (50,320))
    wrong_guess_txt = "  ".join(wrong_guess)
    wrong_guess_txt = textfont.render(wrong_guess_txt,True,tomato)
    screen.blit(wrong_guess_txt, (60,380))  
    life = subfont.render(f"You have {lifecount} chance(s) remaining.", True, tomato)
    screen.blit(life, (50, 450))
    
    pygame.display.update((0,140,size[0],size[1]-150))

    
def endpage(win=False):
    pygame.time.delay(1000)
    screen.fill(purple)
    homepage()
    wintxt = "You won!"
    losttxt = "You lost!"
    
    if win:
        gametxt = subtitlefont.render(wintxt, True, green)
        pygame.mixer.Sound(cdir+"sound_win.wav").play()       
    else:
        gametxt = subtitlefont.render(losttxt, True, green)
        pygame.mixer.Sound(cdir+"sound_lose.wav").play() 
    gametxt2 = subfont.render("Press <Space Bar> to play again", True, green)
    screen.blit(gametxt, (size[0]/2-gametxt.get_width()/2, 320))
    screen.blit(gametxt2, (size[0]/2-gametxt2.get_width()/2, 320+30))
    
    img = hangmanpics[5- lifecount]
    screen.blit(img, (400,size[1] - img.get_height()-20))
    
    if textline > 1:
        for i in range(2):
            text = textfont.render(" ".join(answer[i*split[min_pos]+i : split[min_pos]+i*split[min_pos]+1 ]), True, green)
            screen.blit(text, (50,175+i*65))
    else:
        text = textfont.render(" ".join(answer), True, green)
        screen.blit(text, (50,175))

    pygame.display.update((0,140,size[0],size[1]-150))
    
    restart = True
    while restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "space":
                    restart = False #stop looking into event
    reset()
    
######################
## Inagme-function  ##
######################

def reset():
    '''
    Also choose a new word from word list.
    '''
    global word_lst
    global display_word
    global lifecount
    global guess_lst
    global msg
    global wrong_guess
    global word
    global answer
    
    word = f[random.randrange(0, len(f)-1)][:-1]
    lifecount = 5
    guess_lst = []
    wrong_guess = []
    display_word = []
    word_lst = [i for i in word.upper()]
    msg = ""
    answer = ""
    
    for i in word.upper():
        if i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            display_word.append("_")
        else:
            display_word.append(i)
    answer = "".join(word.upper())
    
def guess(key):
    global word_lst
    global display_word
    global lifecount
    global guess_lst
    global wrong_guess
    key = key.upper()
    
    if key not in guess_lst:
        guess_lst.append(key)
        if key in word_lst:
            msg = "You guessed right!"
            for i in range(len(word_lst)):
                if key == word_lst[i]:
                    display_word[i] = word_lst[i]
        else:
            msg = "Wrong. Try again"
            wrong_guess.append(key)
            lifecount = lifecount - 1
            pygame.mixer.Sound(random.choice([cdir+'sound_wrong1.wav',cdir+'sound_wrong2.wav'])).play()
    else:
        msg = "You have guessed it before. Try another one"
    return msg
 
reset()
while 1:
    homepage()
    ingame()
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key).upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                key = pygame.key.name(event.key)
                msg = guess(key)
            else:
                msg = "Please enter only alphabet letter"
        
        if "_" not in display_word:
            endpage(win=True)
            
        if lifecount == 0:
            endpage()
        
pygame.quit()