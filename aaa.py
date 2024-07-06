from req import generate_prompt_OpenAI
import subprocess
import os
import re
import shutil


def read_base_prompt(character_name):
    base_prompt_path = f'characters/{character_name}/base_prompt.txt'
    if not os.path.exists(base_prompt_path):
        raise FileNotFoundError(f"Base prompt for character {character_name} not found.")
    
    with open(base_prompt_path, 'r', encoding='utf-8') as file:
        base_prompt = file.read().strip()
    
    return base_prompt


def character_generate(character_name, diary, prompt):
    base_prompt = read_base_prompt(character_name)
    s = base_prompt.split('<DIARY_END>')
    full_prompt = s[0]+diary+'\n<DIARY_END>\n'+s[1]
    print('------0')
    response = generate_prompt_OpenAI(full_prompt)
    print('------1')
    
    if "thoughts:" in response and "character_name:" in response:
        thoughts = response.split("thoughts:")[1].split("character_name:")[0].strip()
        character_text = response.split(f"{character_name}:")[1].strip()
    else:
        thoughts = ""
        character_text = response
    
    return thoughts, character_text

def keep_diary(diary, character_name, text):
    new_entry = f'\n{character_name}: {text}<im_end>\n'
    updated_diary = diary + new_entry
    return updated_diary

def execute_command(diary, command):
    parts = command.strip('<>').split('-')
    if len(parts)>=2:
        character_name = parts[0]
        action = parts[1]

        if action == "start":
            _, character_text = character_generate(character_name, diary, '')
            diary = keep_diary(diary, character_name, character_text)
        elif action == "prompt":
            base_prompt = read_base_prompt(character_name)
            diary = keep_diary(diary, 'system', base_prompt)
        elif action == "delete":
            character_path = f'characters/{character_name}'
            if os.path.exists(character_path):
                shutil.rmtree(character_path)
    
    return diary

def analyze_and_execute_commands(diary, text):
    commands = [line for line in text.split('\n') if line.startswith('<') and line.endswith('>')]
    for command in commands:
        diary = execute_command(diary, command)
    return diary

def module_generate(diary, module_name, prompt):
    thoughts, character_text = character_generate(module_name, diary, prompt)
    diary = keep_diary(diary, module_name, character_text)
    diary = analyze_and_execute_commands(diary, character_text)
    return diary, thoughts, character_text

def find_character_names():
    characters = {}
    for root, _, files in os.walk('characters'):
        for file in files:
            if file == 'base_prompt.txt':
                base_file_path = os.path.join(root, file)
                with open(base_file_path, 'r', encoding='utf-8') as base_file:
                    for line in base_file:
                        if line.startswith('<NAMES>'):
                            character_name = os.path.basename(root)
                            names = line.strip().split('<NAMES>')[1].split(',')
                            characters[character_name] = [name.strip() for name in names]
    return characters

def replace_character_names(prompt, character_names):
    replacements = []
    for character_name, aliases in character_names.items():
        for alias in aliases:
            escaped_alias = re.escape(alias)
            if re.search(rf'\b{escaped_alias}\b', prompt, flags=re.IGNORECASE):
                prompt = re.sub(rf'\b{escaped_alias}\b', f'<{character_name}>', prompt, flags=re.IGNORECASE)
                replacements.append(character_name)
    return prompt, replacements

def subtract_text(main_text, sub_text):
    if sub_text in main_text:
        return main_text.replace(sub_text, '', 1)  # Заменяет только первое вхождение
    else:
        return main_text

def user_prompt(diary, prompt):
    print('----asdasd--0')
    character_names = find_character_names()
    
    updated_prompt, replacements = replace_character_names(prompt, character_names)
    diary = keep_diary(diary, 'user', updated_prompt)
    if replacements:
        first_character_name = replacements[0]

        diary, thoughts, character_text = module_generate(diary, first_character_name, '')
        return diary, thoughts, character_text
    
    return diary, "", ""

# Пример использования функций
if __name__ == "__main__":
    prompt = "дворецкий, расскажи че-нить"
    diary = ''
    diary, thoughts, character_text = user_prompt(diary, prompt)
    
    print("Diary:", diary)
    print("Thoughts:", thoughts)
    print("Character Text:", character_text)
