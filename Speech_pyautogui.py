# pyautogui is a lib that controls the functions of the pc, mouse, keyboard, screen etc
import datetime
import os
import pyautogui as pg
import speech_recognition as sr
# keyboard import handles if a key is pressed
import keyboard as key
import time

"""
Speech Recognition so that program can type where I want to go, and select video;
"""

default_desk = 1 # the default desktop number when starting
# 'ctrl + alt' + 'm' to listen
path = r"C:\Users\justi\Desktop\Adv. Py Projects\Keys"
url_head = (400,50)
x,y = url_head
#


def speech_search():

    '''

    :param string: optional
    :return: uses google code from url = "https://pythonspot.com/speech-recognition-using-google-speech-api/#:~:text=Google%20has%20a%20great%20Speech,excellent%20results%20for%20English%20language."
            original code from this website ^

            rest of interaction from oneself
    '''

    import speech_recognition as sr

    # Record Audio with Google's Speech Recognition API code snipet
    # I manipulated the alerts to be used from pg.alert() so it shows up to the user and not in pycharm
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if pg.confirm("Say 'go to ...' or 'open ...' ", title="Speak") == "OK":
            # go to  / will search on chrome
            # open / will open application given name
            # set reminder... / will use pyautogui locate functions to set a reminder in calender
            audio = r.listen(source)
        else:
            exit()
    try:
        # r = r.recognize_google(audio,lang = "en") can interpret language based on the parameter it is given
        # ^ this also returns a string, which is will perform the same function with interpretation of a different lang
        user_speech = r.recognize_google(audio,language="en")

        if str(user_speech).startswith("go to"):
            if pg.confirm("You said: " + user_speech,title="Speech Results") == "OK":
                speech_split = user_speech.split("go to")[-1]
                engine_search(speech_split)
                # voice_key()
            else:
                pass
                # voice_key()
                # pass
        elif str(user_speech).startswith('open'):
            if pg.confirm(f"You said {user_speech}") == 'OK':
                speech_split = user_speech.split("open")[-1]
                app_search(speech_split)
        elif str(user_speech).startswith('reminder'):
            if pg.confirm(f"You said {user_speech}") == "OK":
                # ex. date will return June 7th, which means that I have to split this again to only get 7th
                date = user_speech.split('reminder')[-1]
                # will retrieve the last item of the split string which will be "7th" in this case
                day_num = date.split(' ')[-1]

                try:
                    day_num = int(day_num)
                except ValueError:
                    common_error = "th"
                    if common_error in day_num:
                        day_num = day_num[:-2]
    # date will return ex. " June 7th", so splitting it by the spaces, and using the 2nd item gives me the month name
                month = date.split(' ')[1]
                set_reminder(month,day_num)
        elif str(user_speech).startswith('screenshot'):
            if pg.confirm(f"You said {user_speech}") == "OK":
                screenshot()
        elif str(user_speech).lower() == "add desktop":
            virtual_desktop()
        elif str(user_speech).startswith("image"):
            search = user_speech.split("image")[-1]
            image_search(search)
        elif str(user_speech).startswith("desk"):
            desktopNum = str(user_speech).split("desk ")[-1] # returns the desktop number we want to go to
            navigate_desktops(desktopNum,default_desk)
        elif str(user_speech).lower() == "add desk":
            virtual_desktop()
        else:
            pg.confirm(f"You said {user_speech}")

    except sr.UnknownValueError:
        pg.alert("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        pg.alert("Could not request results from Google Speech Recognition service; {0}".format(e))

def image_search(keyword):
    # hides all applications
    pg.moveTo(1600,880,0.1)
    pg.click()
    # go to chrome browser with coordinates from chrome image
    image = "chrome.png"
    x,y = coords = pg.locateCenterOnScreen(image)
    pg.moveTo(x,y,0.1)
    pg.click()
    pg.hotkey('tab','enter')
    # create new tab
    pg.hotkey('ctrl','t')
    # go to url
    urlLink = "https://www.google.com/search?q={}&rlz=1C1GCEA_enUS935US935&source=lnms&tbm=isch"
    pg.typewrite(urlLink.format(keyword))
    pg.hotkey('enter')

def set_reminder(month,day):
    '''
    will make a reminder in windows calender by navigating to one of the boxes for the days of the month
    :return:
    '''
    # hides all applications
    pg.moveTo(1600,880,0.1)
    pg.click()
    #move to calender
    pg.moveRel(-100,0,0.15)
    pg.click()

    # this will locate the button on screen corresponding to the date given
    # find the date
    time.sleep(0.5)

    month_dictionary = ['january','february','march','april','may','june','july','august',
    'september','october','november','december']

    # month_dictionary = { 1:'january', 2:'february',3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july', 8: 'august',
    #                      9 : 'september', 10: 'october', 11: 'november', 12 : 'december' }

    # gives month in a digit ex 5 or 6
    current_month = time.localtime()[1]

    # checks if destination month is same as the current month
    if month_dictionary[current_month-1] == month.lower():

        for times in range(4):
            pg.press('tab')
        # process to get to the destination key
        for day in range(int(day)-1):
            pg.press('right')
            pg.hotkey('enter')
    else:
        # allows for the month to be changed
        pg.press('tab')
        pg.press('enter')
        time.sleep(0.15)

        for i in range(3):
            time.sleep(0.5)
            pg.press('tab')

        # use the difference in destination month and current month to get to the destined month as int()
        # month_dictionary holds the months in numerical value. Finding the index will return the number month it
        # corresponds to but I have to add an extra one
        destined_month = month_dictionary.index(month.lower())+1
        difference = destined_month - current_month
        print(destined_month)
        print(current_month)
        print(difference)
        time.sleep(0.15)

        for times in range(difference):

            pg.press('right')

        time.sleep(0.15)
        pg.press('enter')
        time.sleep(0.15)

        for day in range(int(day)-1):
            pg.press('right')

        pg.hotkey('enter')
        pg.press("tab")
        # the extra tab is to set the reminder and to place the cursor on the text field


def app_search(keyword):

    pg.moveTo(300,880,0.1)
    pg.click()
    pg.write(keyword,0.1)
    pg.hotkey('enter')

# optional usage of the computer for fun
def paint():
    pass


def navigate_desktops(desktopNum,currentDeskNum):
    # dictionary that changes str to int
    tenNumbers = ["one","two","three","four","five","six","seven","eight","nine","ten"]
    strToNum = {}
    for index in range(0,len(tenNumbers)):
        strToNum[tenNumbers[index]] = index + 1

    # here we can convert it to the integer corresponding and use error handling
    try:
        desktopNum = int(desktopNum)
    except ValueError:
        desktopNum = strToNum[desktopNum]

    # parameter right is default value of False
    if desktopNum > currentDeskNum: # we have to shift right on our desktops
        for desktop in range(desktopNum-currentDeskNum):
            pg.hotkey("win","ctrl","right")
            pg.confirm("Just right")
            currentDeskNum += 1
    elif desktopNum < currentDeskNum:
        for desktop in range(desktopNum-currentDeskNum):
            pg.hotkey("win","ctrl","left")
            pg.confirm("Just Left")
            currentDeskNum -= 1
    else:
        pass

def virtual_desktop():
    global default_desk
    pg.hotkey("win","ctrl","d")
    default_desk += 1
    # this adds a new desktop to the end of the list
    # just like appending an item to the last item

def engine_search(keyword):
    # hides all applications
    pg.moveTo(1600,880,0.1)
    pg.click()
    # go to chrome browser with mouse
    pg.moveTo(520,865,3)
    pg.click()
    pg.hotkey('tab','enter')
    # create new tab
    pg.hotkey('ctrl','t')
    # go to url

    pg.moveTo(x,y,0)
    pg.click()
    pg.typewrite(keyword,interval=0.2)
    pg.hotkey('enter')
    # goes to youtube main page

def screenshot():

    file = "screenshot"+str(datetime.datetime.day)+" "+str(datetime.datetime.hour)+" "+str(datetime.datetime.min)+".png"
    pg.screenshot(file)
    os.open(file)

def calculate():
    # respond and return an answer to a calculation
    pass

# key.read_key() documentation: 'https://www.geeksforgeeks.org/keyboard-module-in-python/'
while True:
    inp_key = key.read_key()
    if inp_key == 'm':
        speech_search()
        inp_key = 0
    else:
        inp_key = 0