from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import json

import brain

import traceback


#load selenium to open a chrome browser with all our cookies/etc to save the hassle
opts = Options()
opts.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
c_driver = """C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"""
driver = webdriver.Chrome(options=opts)
print(driver.title)

#our menu options, 1 and 2 were used for testing purposes, and can help for using it on other sites or if they update the D2L code
def menu():
    print("""
    Choose option:\n
    0) quit\n
    1) download page source\n
    2) search for classname\n
    3) switch frames\n
    4) answer a question\n
    """)
    choice = input("Choice: ")
    if "0" in choice:
        return -1
    elif "1" in choice:
        return 1
    elif "2" in choice:
        return 2
    elif "3" in choice:
        return 3
    elif "4" in choice:
        return 4
    else:
        print("Invalid option")
        return menu()


#set the green outline on the correct answer. Also prints and console.logs the elementID it is changing, in case something goes wrong
def outline(elementID):
    print("setting green outline: " + elementID)
    driver.execute_script("console.log(document.getElementById('"+elementID+"'));document.getElementById('"+elementID+"').style.border = '2px solid green';")

#download the html of the page
def getSource():
    src = driver.page_source
    filename = input("File name to save to: ")
    with open(filename + " (py)", "w") as f:
        f.write(src)

    srcJS = driver.execute_script("return document.documentElement.innerHTML;")
    with open(filename + " (js)", "w") as f:
        f.write(srcJS)

#searches the page for specific classnames
def searchClass():
    cname = input("Classname: ")
    elements = driver.find_elements(By.CLASS_NAME, cname)
    print("Elements found (py): " + str(len(elements)))

    elementsJS = driver.execute_script("return document.getElementsByClassName('"+cname+"').length;")
    print("Elements found (js): " + str(elementsJS))

#answer question menu option, allows you to pick a question (this can be changed to a loop that will answer all questions)
def answerQuestion():
    #if using D2L, you must switch frames into the inner ones to reach the necessary code blocks
    print("make sure you ran switch frames before.")
    try:
        questionIdx = int(input("Enter question number to check: ")) - 1#we subtract one because arrays start at 0, but users shouldn't need to enter 0 for question 1
        print("reading code")
        CODE_TO_RUN = ""
        #reads the JS code that will run to grab every answer/question combo
        with open("./js_script.js", "r") as f:
            CODE_TO_RUN = f.read()
        print("capturing questions")
        #executes the JS in the browser
        questionStr = driver.execute_script(CODE_TO_RUN)
        print(questionStr)
        print("loading questions")
        #load the JSON array into a python one
        questions = json.loads(questionStr)
        print("picking question (" + str(questionIdx) + "/"+str(len(questions))+")")
        question = questions[questionIdx]
        print("answering question")
        #call the api for this question/answer combo
        answers_list = brain.findAnswer(question)
        print("outlining answers")
        #no correct answer found, issue with api or reading them :(
        if (len(answers_list) == 0):
            print("no answers found :/")
        #outline every correct answer
        for i in range(len(answers_list)):
            outline(question["answers"][i]["id"])
        print("done with question!")
    except Exception:#oh no
        traceback.print_exc()
        print("Error")

#switch into the correct frames to be able to access the code blocks that contain the answers/questions
def switchFrames():
    driver.switch_to.frame("content")
    driver.switch_to.frame("pageFrame")


#put the user into the menu, 0 to exit
choice = -2
while (choice != -1):
    if choice != -2:
        if choice == 1:
            getSource()
        elif choice == 2:
            searchClass()
        elif choice == 3:
            switchFrames()
        elif choice == 4:
            answerQuestion()#searchContent()
    choice = menu()
