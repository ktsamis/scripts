from cleverwrap import CleverWrap

"""This script allows you to talk to cleverbot
using an already existing APIKEY in the command line"""

cw = CleverWrap("APIKEY")
question = "nada"
while not question == "finished":
    question = input("You say: ")
    answer = cw.say(question)
    print("The bot says: " + answer)

cw.reset()  # resets the conversation ID and conversation state.

