import random
from io import BytesIO
from threading import Thread
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.messagebox import askquestion
from Marvel import *
from PIL import Image, ImageTk #pip install pillow

name = ""
points = 30
questions = 0
cor_questions = 0
question_done = False
timer = 60


def skipqprompt():
    global points
    prompt = askquestion("Skip question","Are you sure you want to skip this question? It will cost 30 points.",icon='warning')
    if prompt == 'yes':
        points -= 30
        quizquestions.pack_forget()
        showquestion()


def startquiz():
    if len(inputname.get()) >= 1 and inputname.get() != 'Input Username':
        global name
        name = inputname.get()
        showquestion()
    else:
        showinfo(title='Username error', message = 'Please enter a valid username')


def displayhint(AskHint, hint):
    global points
    hintprompt = askquestion("Get hint", 'You sure you want a hint? It will cost 10 points.', icon='warning')
    if hintprompt == 'yes':
        points = points - 10
        hintlabel = Label(master=quizquestions,text = hint,wraplength = 500)
        hintlabel.place(relx=0.5, rely=1, anchor=S)
        AskHint.place_forget()


def showquestion():
    global questions
    global question_done

    if questions <= 9:
        questions += 1
        Startscreen.pack_forget()
        make_quiz_q()# Make thread for the timer
        question_done = False
        timerThread = Thread(target=timer_countdown)
        timerThread.start()
    else:
        global name
        global points
        question_done = True
        saveScore(name, points)
        loadEndscreen()

def loadStartscreen():
    Startscreen.pack()


#check if answer matches chosen character.
def checkanswer(answer="", chosenCharacter=None, timerRanOut=False):
    global points
    global cor_questions
    global question_done

    if timerRanOut:
        showinfo(title='Time\'s up!',
                 message="30 points are deducted and you get your next question")
        points = points - 30
        quizquestions.pack_forget()
        showquestion()
    else:
        if answer != chosenCharacter['character']:
            showinfo(title='Wrong answer',
                     message = "You've submitted an incorrect answer 10 points have been deducted" )
            points = points - 10
        else:
            question_done = True
            showinfo(title='Congratulations',
                     message= "That's the correct answer 25 points have been granted")
            points = points + 25
            cor_questions+= 1
            quizquestions.pack_forget()
            showquestion()


def timer_countdown():
    global timer
    global questions
    while timer >= 1 and not question_done:
        timer = timer-1
        time.sleep(1)
        #timerLabel.config(text="Time: ".format(timer))
    timer = 60

    if not question_done:
        checkanswer(timerRanOut=True)


#clear The asking for username sentence
def Clearinput(event):
    inputname.delete(0, "end")


def loadEndscreen():
    global timer
    timer += 99999999999999999999999999999999999999999999999999999
    Startscreen.pack_forget()
    create_endscreen()
    endscreen.pack()


def make_quiz_q():

    randomOffset = random.randint(0, 500)

    allCharacters = MarvelCharacters(randomOffset)
    print("Choosing character")
    chosenCharacter = chooseCharacter(allCharacters)

    print("making quizquestions")

    #quiz started display question
    quizquestions.pack(fill="both", expand= True)
    quizquestions.config(bg='black')

    #set quiz background
    quizbkgwallpaper = Label(master=quizquestions, image=quizbkg)
    quizbkgwallpaper.pack(side=BOTTOM)

    #points displayed on screen
    currentpoints = Label (master=quizquestions,text="Current amount of points:{}".format(points),background ='#ff8400')
    currentpoints.place(relx= 0.15,rely=0.01, anchor=CENTER)

    # points displayed on screen
    #timerLabel.place(relx=1, rely=0.01, anchor=CENTER)

    #question header is incorporated into background, because Label lacks the transparant background

    #Insert picture into frame
    URL = chosenCharacter["imageUrl"]
    try:
        print("Getting image")
        u = urlopen(URL)
        raw_data = u.read()
        u.close()
    except HTTPError as e:
        # do something
        print('Error code: ', e.code)
    except URLError as e:
        # do something
        print('Reason: ', e.reason)
    else:
        # do something
        print('good!')

    im = Image.open(BytesIO(raw_data))
    im = im.resize((200,200))
    photo = ImageTk.PhotoImage(im)

    label = Label(master = quizquestions,image=photo)
    label.image = photo
    label.place(relx=0.5, rely = 0.5, anchor=CENTER)

    hint = giveHint(chosenCharacter)

    optionlist = options(allCharacters, chosenCharacter)
    print(optionlist)

    textoptionA = optionlist[0]
    textoptionB = optionlist[1]
    textoptionC = optionlist[2]
    textoptionD = optionlist[3]

    optionA = Button(master=quizquestions, text=textoptionA, anchor=W, command=lambda: checkanswer(textoptionA, chosenCharacter))
    optionA.config(width=15)
    optionA.place(relx=0.15, rely=0.35, anchor=CENTER)

    optionB = Button(master=quizquestions, text=textoptionB, anchor=W, command=lambda: checkanswer(textoptionB, chosenCharacter))
    optionB.config(width=15)
    optionB.place(relx=0.15, rely=0.65, anchor=CENTER)

    optionC = Button(master=quizquestions, text=textoptionC, anchor=W, command=lambda: checkanswer(textoptionC, chosenCharacter))
    optionC.config(width=15)
    optionC.place(relx=0.85, rely=0.35, anchor=CENTER)

    optionD = Button(master=quizquestions, text=textoptionD, anchor=W, command=lambda: checkanswer(textoptionD, chosenCharacter))
    optionD.config(width=15)
    optionD.place(relx=0.85, rely=0.65, anchor=CENTER)

    AskHint = Button(master=quizquestions,
                     text='I need a H-I-N-T',
                     font=('Elephant',25,'italic'),
                     command=lambda: displayhint(AskHint, hint))
    AskHint.config(width=500)
    AskHint.place(relx=0.5, rely=1, anchor=S)

    skip_button = Button(master=quizquestions,text="Skip", command=skipqprompt)
    skip_button.place(relx=0.95,rely=0.1, anchor=N)


def create_endscreen():
    #create endscreen with info and highscores

    endscreen.pack(fill="both", expand=True)

    higscorebkgwallpaper = Label(master=endscreen, image=highscorebkg)
    higscorebkgwallpaper.pack(side=BOTTOM)

    highscore = loadHighScore()

    highscores = Label(master=endscreen,
                       background='#fefefe',
                       text=highscore,
                       foreground = "#ff0000",
                       font =('Lucida Console',10,'bold'))
    highscores.place(relx=0.3, rely= 0.35, anchor=CENTER)


#creating the main window and fixing it's size
gamewd = Tk()
icon = PhotoImage(file='GUI\\icon.png')
gamewd.tk.call('wm', 'iconphoto', gamewd._w, icon)
gamewd.title("Super Quizz")
gamewd.geometry("500x500")
gamewd.resizable(0,0)


#creating start frame
Startscreen = Frame(master=gamewd)
Startscreen.pack(fill="both",expand = True)

#creating quiz frame
quizquestions = Frame(master=gamewd)

#creating end frame
endscreen = Frame(master=gamewd)


#set image as background in startscreen
bkg = PhotoImage(file="GUI\\bkgmarvel.png")
bkgwallpaper = Label(master=Startscreen, image=bkg)
bkgwallpaper.pack(side=BOTTOM)

#specifying start frame containments
header = Label(master=Startscreen,
               text= "Super Quizz\n The G A M E",
               background = 'black',
               foreground = '#2CADE9',
               font=('Elephant',25,'bold'))

#place header
header.place(relx=0.5, rely=0.1, anchor=CENTER)

#Input bar to save username
inputname = Entry(master=Startscreen)
inputname.insert(0,'Input Username')
inputname.place(relx=0.5, rely=0.5, anchor=CENTER)

#if Left mouse button preseed clear inputname
inputname.bind("<Button-1>", Clearinput)


#startquizbutton on startscreen
startquizbutton = Button(master=Startscreen,text = 'Start quiz',command=startquiz)
startquizbutton.place(relx=0.5,rely=0.6,anchor=CENTER)

quizbkg = PhotoImage(file="GUI\\quizbkg.png")
highscorebkg = PhotoImage(file="GUI\\highscores.png")

#timerLabel = Label(master=quizquestions, text="Time: ", background='#ff8400')
#timerLabel.place(relx=5.5, rely=5.01, anchor=CENTER)

gamewd.mainloop()