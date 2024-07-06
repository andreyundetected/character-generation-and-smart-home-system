import subprocess
import speech_recognition as sr
import pyttsx3
import time

def generate_token(model_path, prompt, temperature, cfg_negative_prompt, threads, n_predict, ctx_size, batch_size, ubatch_size):
    set_path_command = 'set PATH=C:\\msys64\\mingw64\\bin;%PATH%'
    main_command = [
        'C:\\MyProjects\\llama.cpp\\main.exe',
        '-m', f'"{model_path}"',
        '-p', f'"{prompt}"',
        '--temp', str(temperature),
        '--cfg-negative-prompt', f'"{cfg_negative_prompt}"',
        '--special',
        '-t', str(threads),
        '-n', str(n_predict),
        '-c', str(ctx_size),
        '-b', str(batch_size),
        '-ub', str(ubatch_size)
    ]
    
    full_command = f"{set_path_command} && {' '.join(main_command)}"
    
    result = subprocess.run(full_command, capture_output=True, text=True, shell=True)
    
    if result.returncode != 0:
        print("Error:", result.stderr)
    return result.stdout.strip()

def generate_until_eos(model_path, initial_prompt, temperature, cfg_negative_prompt):
    generated_text = initial_prompt
    while True:
        token = generate_token(
            model_path=model_path,
            prompt=generated_text,
            temperature=temperature,
            cfg_negative_prompt=cfg_negative_prompt,
            threads=2,
            n_predict=1,
            ctx_size=0,
            batch_size=2048,
            ubatch_size=512
        )
        
        print(token, end='', flush=True)
        
        if token.endswith('<|endoftext|>') or not token:
            break
        
        generated_text += token

    return generated_text

def listen_for_prompt(timeout=2, language="en-US"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю вас...")
        audio = recognizer.listen(source, timeout=timeout)
    try:
        prompt = recognizer.recognize_google(audio, language=language)
        print("Вы сказали: " + prompt)
        return prompt
    except sr.UnknownValueError:
        print("Не удалось распознать речь.")
        return ""
    except sr.RequestError as e:
        print("Ошибка сервиса распознавания; {0}".format(e))
        return ""

def speak_text(text, language="en"):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if language == "ru":
        for voice in voices:
            if "russian" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    else:
        for voice in voices:
            if "english" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    model_path = 'C:/MyProjects/llama.cpp/models/Hermes-2-Pro-Llama-3-8B-Q6_K.gguf'
    language = "en-US"
    prompt = listen_for_prompt(timeout=2, language=language)
    if prompt:
        temperature = 0.8
        cfg_negative_prompt = ""
        output = generate_until_eos(model_path, prompt, temperature, cfg_negative_prompt)
        print("\nGenerated Text:")
        print(output)
        speak_text(output, language="en" if language == "en-US" else "ru")
