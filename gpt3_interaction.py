import requests  # Import the requests library
import config


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
    user_input = input("Enter a prompt for GPT-3: ")
    gpt3_response = send_to_openai_gpt3(user_input)
    if gpt3_response:
        print("GPT-3 response:", gpt3_response)
