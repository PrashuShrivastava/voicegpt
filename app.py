from flask import Flask, render_template
import speech_recognition as sr

app = Flask(__name)

# Initialize the recognizer
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000  # Adjust as needed

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
