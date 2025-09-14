import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3

# Initialize speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def get_audio():
    """Listen to microphone and convert speech to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="🎙 Listening...")
        root.update()
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        status_label.config(text=f"✅ You said: {text}")
        root.update()
        return text.lower()
    except sr.UnknownValueError:
        status_label.config(text="❌ Could not understand speech.")
        speak("Sorry, I could not understand.")
        return None
    except sr.RequestError:
        status_label.config(text="❌ Speech recognition service error.")
        speak("Speech service error.")
        return None

def calculate(expression):
    """Perform calculation from spoken expression"""
    try:
        expression = expression.replace("plus", "+")
        expression = expression.replace("minus", "-")
        expression = expression.replace("into", "*")
        expression = expression.replace("times", "*")
        expression = expression.replace("multiplied by", "*")
        expression = expression.replace("divide", "/")
        expression = expression.replace("divided by", "/")
        result = eval(expression)
        return result
    except:
        return None

def voice_calculate():
    user_input = get_audio()
    if user_input:
        if "stop" in user_input or "exit" in user_input or "quit" in user_input:
            speak("Goodbye!")
            root.destroy()
            return
        result = calculate(user_input)
        if result is not None:
            result_label.config(text=f"🧮 Result: {result}")
            speak(f"The result is {result}")
        else:
            result_label.config(text="⚠ Could not calculate that.")
            speak("Sorry, I could not calculate that.")

def clear_result():
    result_label.config(text="")
    status_label.config(text="")

# --- GUI Setup ---
root = tk.Tk()
root.title("Voice Controlled Calculator")
root.geometry("400x300")
root.config(bg="#f4f4f4")

title_label = tk.Label(root, text="🎙 Voice Calculator", font=("Arial", 18, "bold"), bg="#f4f4f4")
title_label.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 10), fg="blue", bg="#f4f4f4")
status_label.pack()

result_label = tk.Label(root, text="", font=("Arial", 14), fg="green", bg="#f4f4f4")
result_label.pack(pady=20)

speak_button = tk.Button(root, text="🎤 Speak", command=voice_calculate, font=("Arial", 12), bg="#4CAF50", fg="white", width=15)
speak_button.pack(pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_result, font=("Arial", 12), bg="#f44336", fg="white", width=15)
clear_button.pack()

exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Arial", 12), bg="#333333", fg="white", width=15)
exit_button.pack(pady=10)

root.mainloop()
