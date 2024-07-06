import requests


def generate_prompt_server(prompt):
    url = 'http://18.185.231.201/generate'

    #prompt = f"GPT4 Correct User: {prompt}<|end_of_turn|>GPT4 Correct Assistant:"
    params = {
        "prompt": prompt,
        "password": 'COINIS_LLM_SERVER_18180',
        "num_token": "2048",
    }
    response = requests.post(url, json=params)
    if response.status_code == 200:
        print(str(response.json()['response']))
        print('-=-=-=-=-')
        print(str(response.json()['response']).replace(prompt.replace('<im_end>',' '),''))
        print('-=-=-ajsdalskdl=-=-')
        print(prompt)
        return (str(response.json()['response'])).replace(prompt.replace('<im_end>',' '),'')
    else:
        return "error:", response.status_code, response.text
    







import json
from datetime import datetime
import base64
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import mss
import openai
api_key = ""

# Function to encode the image from PIL image to base64
def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to generate prompt with image
def generate_prompt_with_image(prompt_text, image,MT):
    base64_image = encode_image(image)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": MT
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

# Function to generate prompt without image
def generate_prompt_without_image(prompt_text,MT):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        "max_tokens": MT
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

# Function to count tokens (approximation)
def count_tokens(text):
    tokens = text.split()
    return len(tokens)



def write_log(prompt, img, r):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response_content = r['choices'][0]['message']['content'].replace('\n\n','\n')

    # Читаем текущие значения токенов из файла
    try:
        with open("openai_logs.txt", "r", encoding='utf-8') as file:
            lines = file.readlines()
            total_prompt_tokens = int(lines[0].strip())
            total_completion_tokens = int(lines[1].strip())
    except (FileNotFoundError, IndexError):
        total_prompt_tokens = 0
        total_completion_tokens = 0
    except UnicodeDecodeError:
        print("Ошибка декодирования файла, файл содержит некорректные символы")
        total_prompt_tokens = 0
        total_completion_tokens = 0
        lines = []

    # Обновляем суммы токенов
    total_prompt_tokens += r['usage']['prompt_tokens']
    total_completion_tokens += r['usage']['completion_tokens']

    # Записываем обновленные значения токенов и данные запроса
    with open("openai_logs.txt", "w", encoding='utf-8') as file:
        file.write(f"{total_prompt_tokens}\n")
        file.write(f"{total_completion_tokens}\n")
        for line in lines[2:]:  # Сохраняем предыдущие логи
            file.write(line)
        # Добавляем новую запись
        file.write(f"\n\n\n=={now}==\n")
        file.write(f"PROMPT: {prompt}\n")
        file.write(f"IMG: {bool(img)}\n")
        file.write(f"RESPONSE: {response_content}\n\n")




# Example usage
def generate_prompt_OpenAI(text, img = None, MT = 4096):
    if img:
        response = generate_prompt_with_image(text, img, MT)
    else:
        response = generate_prompt_without_image(text, MT)
    
    write_log(text, img, response)

    return response['choices'][0]['message']['content']
    



