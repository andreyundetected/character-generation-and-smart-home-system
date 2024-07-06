import subprocess

def generate_token(model_path, prompt, temperature, cfg_negative_prompt, threads, n_predict, ctx_size, batch_size, ubatch_size):
    print('start')
    # Установим переменную PATH и затем запустим команду
    set_path_command = 'set PATH=C:\\msys64\\mingw64\\bin;%PATH%'
    main_command = f'C:\\MyProjects\\llama.cpp\\main.exe -m "{model_path}" -p "{prompt}" -n {n_predict}'
    
    full_command = f'{set_path_command} && {main_command}'
    
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
            threads=16, # Укажите нужное количество потоков
            n_predict=1,
            ctx_size=0,
            batch_size=2048,
            ubatch_size=512
        )
        
        print(token, end='', flush=True)  # Выводим каждый токен сразу же
        
        if token.endswith('<|im_end|>') or not token:  # Проверяем на энд токен или пустую строку
            break
        
        generated_text += token  # Добавляем сгенерированный токен к основному тексту

def generate_prompt(prompt, model='Hermes-2-Pro-Llama-3-8B-Q6_K'):
    return generate_until_eos(f'C:/MyProjects/llama.cpp/models/{model}.gguf', f"GPT4 Correct User: {prompt} \n\n\n write '<|im_end|>' for end\n\n\nGPT4 Correct Assistant:", 0.8, '')



if __name__ == "__main__":
    print(generate_prompt('Hello!'))
