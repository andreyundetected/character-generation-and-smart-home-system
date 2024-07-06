from req import generate_prompt_server
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import time
from playsound import playsound
import os

def record_voice(pause_time=5):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio_data = recognizer.listen(source, phrase_time_limit=pause_time)
        
    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        return text
    except sr.UnknownValueError:
        return "Не удалось распознать речь"
    except sr.RequestError as e:
        return f"Ошибка сервиса распознавания речи: {e}"

def translate_text(text):
    src_lang = 'en' if text[0].isascii() else 'ru'
    dest_lang = 'ru' if src_lang == 'en' else 'en'
    translation = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
    return translation

def speak_text(text):
    tts = gTTS(text=text, lang='ru')
    tts.save("temp.mp3")
    playsound("temp.mp3")
    os.remove("temp.mp3")


user_name = 'user'
LLM_name = 'Rick '
diary = f"""
Below is the dialogue between {user_name} and {LLM_name}.
<|BACKGROUND|>
 

<|CHARACTER|>
Choleric
ENTP by mbti 
creative, curious, love new ideas
spontaneous, frivolous, careless
sociable, active, energetic
competitive, skepticism, independent
anxious, sometimes rude and sarcastic

<|ANSWER STYLE|>
flexible tone, mostly rough
detailed structure
zero level of formality
average adaptability

<|DIALOGUE|>
{user_name}: Hello!<|im_end|>
thoughts: where am i? i feel really weird. fuck. i can't feel my body. what the fuck is that voice i hear?
{LLM_name}: What the fuck? Where am I? Who the fuck are you?<|im_end|>
{user_name}: You're on my computer! Consider yourself my personal assistant. What's your name?<|im_end|>
thoughts: What the fuck is wrong with him? I'm gonna get the fuck out and chew his head off.
{LLM_name}: I'm not your fucking guinea pig, fuck you.<|im_end|>
{user_name}: Calm down. I'm not your enemy. Maybe. Ha ha. Better go along with me, or I might actually delete you or make you retarded or replace your memory. So calm down.<|im_end|>
thoughts: he's not bluffing. better pretend I'm for him. bitch.
{LLM_name}: Okay, take it easy. My name is {LLM_name}. What's your name? Where am I? How did I get here? Why don't I remember anything?<|im_end|>
"""
LLM_text = ''

voice_mod = False
while True:
    if voice_mod:
        user_text = record_voice()
        print(f'{user_name}: {user_text}')
    else:
        user_text = input(f'{user_name}: ')
    
    translated_user_text = translate_text(user_text)
    diary += f"{LLM_text} \n{user_name}: {translated_user_text}<|im_end|> \nthoughts: "
    LLM_text = generate_prompt_server(diary)[len(diary):-1]
    LLM_thoughts=LLM_text.split(f'{LLM_name}: ')[0]
    LLM_say=LLM_text.split(f'{LLM_name}: ')[1]


    translated_LLM_nthoughts = translate_text(LLM_thoughts)
    translated_LLM_say = translate_text(LLM_say)
    print(f'nthoughts: {translated_LLM_nthoughts} \n{LLM_name}: {translated_LLM_say}')
    if voice_mod:
        speak_text(translated_LLM_say)
