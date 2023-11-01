from gpt3_interaction import send_to_openai_gpt3
from flask import Flask, render_template, request
import speech_recognition as sr
import requests
import openai
import time

# Set your OpenAI API key
import config

# Initialize the recognizer
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300  # Adjust as needed

# Set up OpenAI API key
openai.api_key = config.openai_api_key  # Replace with your API key


def listen_and_convert_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(
                source, timeout=10
            )  # Listen for 10 seconds, adjust as needed
            text = recognizer.recognize_google(audio)
            print("Spoken text:", text)  # Print the spoken text

            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None


# def send_to_openai_gpt3(text):
#     if text:
#         response = openai.Completion.create(
#             engine="davinci",
#             prompt=text,
#             max_tokens=50,
#         )

#         generated_text = response.choices[0].text
#         print("Generated text from GPT-3:", generated_text)
#         return generated_text
#     else:
#         return None

if __name__ == "__main__":
    while True:
        spoken_text = listen_and_convert_to_text()
        if spoken_text:
            gpt3_response = send_to_openai_gpt3(spoken_text)
            # You can use gpt3_response as needed in your application

            # Wait for 5 seconds before listening again, adjust as needed
            time.sleep(10)
