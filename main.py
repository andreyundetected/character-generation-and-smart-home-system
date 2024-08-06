import os
from req import generate_prompt_OpenAI

def keep_diary(diary, character_name, text):
    new_entry = f'\n{character_name}: {text}\n\n\n'
    updated_diary = diary + new_entry
    return updated_diary

def load_prompts(directory):
    prompts = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'base_prompt.txt':
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    prompts[root] = f.readlines()
    return prompts

def find_triggered_characters(prompt, diary, prompts):
    triggered_characters = []
    character_order = []

    for character_path, lines in prompts.items():
        for line in lines:
            if line.startswith('<NAMES>'):
                trigger_phrases = line[len('<NAMES>'):].strip().split(', ')
                for phrase in trigger_phrases:
                    if phrase in prompt or phrase in diary:
                        character_name = os.path.basename(character_path)
                        if character_name not in character_order:
                            character_order.append((character_name, prompt.find(phrase), diary.find(phrase)))

    character_order.sort(key=lambda x: (x[1] if x[1] != -1 else float('inf'), x[2] if x[2] != -1 else float('inf')))

    triggered_characters = [name for name, _, _ in character_order]
    print(triggered_characters)
    return triggered_characters


def generate_prompt(diary, character):
    print(character)
    base_prompt_path = f'characters/{character}/base_prompt.txt'
    if os.path.exists(base_prompt_path):
        with open(base_prompt_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        if character == 'butler':
            lines = update_butler_list(load_prompts('characters'), 'Список всех личностей:', 'Список всех помощников:').split('\n')
        

        new_prompt = []
        in_diary_section = False
        for line in lines:
            if '<DIARY_START>' in line:
                in_diary_section = True
                new_prompt.append('<DIARY_START>\n')
                new_prompt.append(diary + '\n')
            elif '<DIARY_END>' in line:
                in_diary_section = False
                new_prompt.append('<DIARY_END>\n')
            elif not in_diary_section:
                new_prompt.append(line)
        
        generated_prompt = ''.join(new_prompt)
        print(new_prompt)
        response = generate_prompt_OpenAI(generated_prompt)
        #response = 'a'
        diary = keep_diary(diary, character, response.split(' | ')[-1].replace('***',''))
        return diary
    return diary
"""
def process_commands(response, diary):
    commands = []
    while '<' in response and '>' in response:
        start_idx = response.index('<')
        end_idx = response.index('>')
        command = response[start_idx:end_idx+1]
        commands.append(command)
        response = response[end_idx+1:]

    for command in commands:
        if command.startswith('<*') and command.endswith('-start>'):
            character_to_start = command[2:-7]
            response, diary = generate_prompt(diary, character_to_start)
            diary = process_commands(response, diary)

    return diary
"""
def update_butler_list(prompts, label_personalities, label_assistants):
    personalities_list = []
    assistants_list = []
    
    for character_path, lines in prompts.items():
        character_name = os.path.basename(character_path)
        summary = ""
        in_summary_section = False
        
        for line in lines:
            if '<SUMMARIZE_START>' in line:
                in_summary_section = True
            elif '<SUMMARIZE_END>' in line:
                in_summary_section = False
            elif in_summary_section:
                summary += line.strip() + " "
        
        for line in lines:
            if '<CASTE> personality' in line and 'creator of personalities' not in character_path:
                personalities_list.append(f"<{character_name}> - {summary.strip()}")
            elif '<CASTE> assistant' in line and 'creator of assistants' not in character_path:
                assistants_list.append(f"<{character_name}> - {summary.strip()}")
    butler_prompt_path = 'characters/butler/base_prompt.txt'
    if os.path.exists(butler_prompt_path):
        with open(butler_prompt_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        updated_prompt = []
        for line in lines:
            updated_prompt.append(line)
            if label_personalities in line:
                updated_prompt.append('\n'.join(personalities_list) + '\n')
            if label_assistants in line:
                updated_prompt.append('\n'.join(assistants_list) + '\n')

    #print(''.join(updated_prompt))
    return ''.join(updated_prompt)

def character_generate(diary, characters):
    for character in characters:
        diary = generate_prompt(diary, character)

    return diary

def process_user_input(prompt, diary):
    prompts = load_prompts('characters')
    diary = keep_diary(diary, 'user', prompt)
    triggered_characters = find_triggered_characters(prompt, diary, prompts)
    diary = character_generate(diary, triggered_characters)
    return diary

# Пример использования функции
user_text = "chunga и дворецкий. знаете ли вы персонажа 'Аке' ?"
user_diary = ""
print(process_user_input(user_text, user_diary))
