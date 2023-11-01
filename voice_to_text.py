import speech_recognition as sr
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from gpt3_interaction import send_to_openai_gpt3


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
                # socketio.emit("response", text)
                # Simulate GPT-3 response (replace this with your actual GPT-3 logic)
                gpt3_response = send_to_openai_gpt3(text)
                socketio.emit("response", gpt3_response)
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


if __name__ == "__main__":
    # Start the Flask-SocketIO server
    socketio.run(app)
