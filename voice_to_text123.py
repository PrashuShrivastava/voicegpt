# import speech_recognition as sr
# from flask import Flask, render_template, send_from_directory
# from flask_socketio import SocketIO
# from gpt3_interaction import send_to_openai_gpt3


# # Initialize the Flask app and SocketIO
# app = Flask(__name__)
# socketio = SocketIO(app)
# app.config["UPLOAD_FOLDER"] = "static"  # Set your static folder name


# # Initialize the recognizer
# recognizer = sr.Recognizer()
# recognizer.energy_threshold = 300  # Adjust as needed
# listening = False  # Flag for listening state
# microphone = sr.Microphone()  # Store the microphone instance


# @app.route("/static/<filename>")
# def serve_static(filename):
#     return send_from_directory("static", filename)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @socketio.on("start_listening")
# def start_listening():
#     global listening, microphone
#     if not listening:
#         with sr.Microphone() as source:
#             print("Listening...")
#             listening = True
#             microphone = source  # Store the microphone instance
#             try:
#                 audio = recognizer.listen(source, timeout=10)
#                 text = recognizer.recognize_google(audio)
#                 print("Spoken text:", text)  # Print the spoken text
#                 # socketio.emit("response", text)
#                 # Simulate GPT-3 response (replace this with your actual GPT-3 logic)
#                 gpt3_response = send_to_openai_gpt3(text)
#                 socketio.emit("response", gpt3_response)
#             except sr.UnknownValueError:
#                 print("Could not understand audio")
#             except sr.RequestError as e:
#                 print(f"Could not request results; {e}")
#         listening = False


# @socketio.on("stop_listening")
# def stop_listening():
#     global listening, microphone
#     listening = False
#     if microphone:
#         microphone.__exit__(None, None, None)


# if __name__ == "__main__":
#     # Start the Flask-SocketIO server
#     socketio.run(app)


import speech_recognition as sr
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import requests  # Import the requests library
import os
import config  # Assuming you have a 'config.py' file with your API key

# Initialize the Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)
app.config["UPLOAD_FOLDER"] = "static"  # Set your static folder name

# Initialize the recognizer
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300  # Adjust as needed
listening = False  # Flag for listening state
microphone = sr.Microphone()  # Store the microphone instance


@app.route("/static/<filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("start_listening")
def start_listening():
    global listening, microphone
    if not listening:
        with sr.Microphone() as source:
            print("Listening...")
            listening = True
            microphone = source  # Store the microphone instance
            try:
                audio = recognizer.listen(source, timeout=10)
                text = recognizer.recognize_google(audio)
                print("Spoken text:", text)  # Print the spoken text
                # Send spoken text to GPT-3 and get a response
                gpt3_response = send_to_openai_gpt3(text)
                socketio.emit("response", text)  # Emit the spoken text
                socketio.emit("response", gpt3_response)  # Emit the GPT-3 response
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        listening = False


@socketio.on("stop_listening")
def stop_listening():
    global listening, microphone
    listening = False
    if microphone:
        microphone.__exit__(None, None, None)


def send_to_openai_gpt3(text):
    if text:
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.openai_api_key}",  # Set your API key
        }

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": text}],
            "temperature": 0.7,
            "stream": True,  # Stream results
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            generated_text = data["choices"][0]["message"]["content"]
            print("Generated text from GPT-3:", generated_text)
            return generated_text
        else:
            print(f"API request failed with status code: {response.status_code}")
            return None
    else:
        return None


if __name__ == "__main__":
    # Start the Flask-SocketIO server
    socketio.run(app)
