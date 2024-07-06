import subprocess
import datetime

def generate_with_hf_repo(prompt, model_path = 'C:/MyProjects/llama.cpp/models/Hermes-2-Pro-Llama-3-8B-Q6_K.gguf'):
    set_path_command = 'set PATH=C:\\msys64\\mingw64\\bin;%PATH%'
    main_command = f'C:\\MyProjects\\llama.cpp\\main.exe -m "{model_path}" -p "{prompt}" -n {-1}'
    
    full_command = f'{set_path_command} && {main_command}'
    
    result = subprocess.run(full_command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print("Error (stderr):", result.stderr)
    print("Output (stdout):", result.stdout)
    return result.stdout.strip().split(' B:')[-1]

if __name__ == "__main__":
    prompt = input()
    prompt = f"A:Hi<|im_end|> B:Hello!<|im_end|> A:{prompt}<|im_end|> B:"
    print(datetime.datetime.now())
    print(generate_with_hf_repo(prompt))
    print(datetime.datetime.now())
