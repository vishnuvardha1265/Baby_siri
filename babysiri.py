import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import datetime
import webbrowser
import threading
import os
import time
import uuid

# Speak using gTTS
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = f"temp_audio_{uuid.uuid4()}.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

# Listen to user's voice
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
            command = r.recognize_google(audio, language='en-in')
            return command.lower()
        except:
            return ""

# Process the command
def assistant_response(command):
    if 'what is time' in command:
        response = datetime.datetime.now().strftime("The time is %I:%M %p")
    elif 'today date' in command:
        response = datetime.date.today().strftime("Today is %B %d, %Y")
    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        response = "Opening Google"
    elif 'open leetcode' in command:
        webbrowser.open("https://leetcode.com")
        response = "Opening LeetCode"
    elif 'open hackerrank' in command:
        webbrowser.open("https://www.hackerrank.com")
        response = "Opening HackerRank"
    elif 'open w3schools' in command:
        webbrowser.open("https://www.w3schools.com")
        response = "Opening W3Schools"
    elif 'open github' in command:
        webbrowser.open("https://github.com")
        response = "Opening GitHub"
    elif 'climate' in command:
        webbrowser.open("https://www.google.com/search?q=weather+in+my+location")
        response = "Showing climate in your browser"
    elif 'what is your name' in command:
        response = "I am your Baby Siri Voice Assistant"
    elif 'play music' in command:
        speak("Which song would you like to play?")
        song = listen()
        response = f"Playing {song} on YouTube"
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
    elif 'stop' in command or 'exit' in command:
        response = "Goodbye!"
        assistant_logs.append(("🗣️ You", command))
        assistant_logs.append(("🤖 Siri", response))
        speak(response)
        return False
    else:
        response = "Sorry, I can't do that yet."

    assistant_logs.append(("🗣️ You", command))
    assistant_logs.append(("🤖 Siri", response))
    speak(response)
    return True

# Background assistant loop
def run_assistant():
    greeting = "Hello, I am your Baby Siri. How can I help you?"
    speak(greeting)
    assistant_logs.append(("🤖 Siri", greeting))

    while True:
        command = listen()
        if not command:
            continue
        if not assistant_response(command):
            break
        time.sleep(1)

# Streamlit setup
st.set_page_config(page_title="Baby Siri", page_icon="🎤")
st.title("🎤 Baby Siri - Voice Assistant")

# Show available voice commands
commands = [
    "what is time",
    "today date",
    "open google",
    "open leetcode",
    "open hackerrank",
    "open w3schools",
    "open github",
    "climate",
    "what is your name",
    "play music",
    "stop / exit"
]

st.markdown("#### 💡 Available Voice Commands:")
st.code(", ".join(commands), language="markdown")


if 'started' not in st.session_state:
    st.session_state.started = False
if 'log' not in st.session_state:
    st.session_state.log = []

assistant_logs = st.session_state.log

if st.button("▶️ Start Listening"):
    if not st.session_state.started:
        st.session_state.started = True
        threading.Thread(target=run_assistant, daemon=True).start()
        st.success("Voice assistant started!")

if st.button("🛑 Stop Assistant"):
    st.session_state.started = False
    st.warning("Assistant stopped.")
# Text input alternative for voice commands
st.markdown("#### 📝 Type a Command Instead:")
text_command = st.text_input("Enter your command below and press Enter:")

if text_command:
    if assistant_response(text_command.lower()):
        st.session_state.log = assistant_logs  # Update the log
        st.experimental_rerun()


st.markdown("---")
st.subheader("📝 Chat Log")
for speaker, text in assistant_logs:
    st.write(f"**{speaker}**: {text}")
