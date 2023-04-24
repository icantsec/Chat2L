import openai

#create the prompt for the question object (formats the query so it should return only number(s) for the correct choice(s)
def getPrompt(question):
    to_send = question["question"]["text"] + "\n"
    counter = 1
    correct_nums = []
    for i in range(len(question["answers"])):
        to_send += str(counter) + ") " + question["answers"][i]["text"] + "\n"
        counter += 1
    to_send += "answer number(s) only"
    return to_send

#make the request to the API. You can change the max_tokens/temperature/model here
def makeRequest(inp):
    openai.api_key = "API_KEY_HERE"
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=inp,
    max_tokens=256,
    temperature=0
    )
    return response["choices"][0]["text"]

#creates the prompt based on the question object that is passed in, sends it to the api, and returns the correct answer number(s)
def findAnswer(question):
    prompt = getPrompt(question)
    response = makeRequest(prompt)
    cleaned = response.strip()
    correct_opts = [int(ch) for ch in cleaned if ch.isdigit()]
    return correct_opts

#used to run a test question to check that the API is working, not ran by default
def testquest():
    question = {
        "question": {"text": "Which word(s) start with an A?"},
        "answers": [
            {"text": "Soup"},
            {"text": "Alphabet"},
            {"text": "Words"},
            {"text": "Another"}
        ]
    }
    answers = findAnswer(question)
    return answers

#testquest()
