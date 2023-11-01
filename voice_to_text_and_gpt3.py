import speech_recognition as sr
import requests
import openai

# Set your OpenAI API key
import config

# Initialize the recognizer
recognizer = sr.Recognizer()

def listen_and_convert_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)  # You can use other engines as well
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def send_to_openai_gpt3(text):
    if text:
        response = openai.Completion.create(
            engine="davinci",  # You can choose a different engine based on your needs
            prompt=text,
            max_tokens=50,    # Adjust the max_tokens as needed
        )

        generated_text = response.choices[0].text
        print("Generated text from GPT-3:", generated_text)
        return generated_text
    else:
        return None

if __name__ == "__main__":
    while True:
        spoken_text = listen_and_convert_to_text()
        if spoken_text:
            gpt3_response = send_to_openai_gpt3(spoken_text)
            # You can use gpt3_response as needed in your application
