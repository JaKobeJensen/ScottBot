from scottbot import ScottBot
import keyboard
import numpy as np
from rich import print
import os


def main():
    os.system("cls")
    scottbot = ScottBot()
    print("[green]Press 't' to ask ScottBot a question")
    print("[red]Press 'q' to quit\n")
    while True:
        if keyboard.is_pressed("t"):
            scottbot.ask_question()
            print("[green]Press 't' to ask ScottBot a question")
            print("[red]Press 'q' to quit\n")
        elif keyboard.is_pressed("q"):
            return
        
        
def test_listen():
    scottbot = ScottBot()
    text = scottbot.listen()
    print(text)
    return

def test_answer_question():
    scottbot = ScottBot()
    question = "What is a cow?"
    response = scottbot.answer_question(question=question)
    np.save("audio", response["audio"], True)
    print(response["text"])
    return

def test_speak():
    scottbot = ScottBot()
    audio = np.load("audio.npy")
    scottbot.speak_from_audio_data(audio)
    scottbot.speak_from_audio_file("audio.wav")
    return

def test_ask_question():
    scottbot = ScottBot()
    response = scottbot.ask_question()
    return

if __name__ == "__main__":
    # test_listen()
    # test_answer_question()
    # test_speak()
    # test_ask_question()
    main()
    quit()
