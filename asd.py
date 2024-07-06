import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3
import time

def record_voice(pause_time=2):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio_data = recognizer.listen(source, phrase_time_limit=pause_time)
        
    try:
        print("Recognizing...")
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
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Установить скорость речи
    engine.setProperty('voice', 'ru')  # Установить язык речи
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        recorded_text = record_voice()
        if recorded_text:
            print(f"Распознанный текст: {recorded_text}")
            translated_text = translate_text(recorded_text)
            print(f"Перевод: {translated_text}")
            speak_text(translated_text)
        time.sleep(5)  # Пауза между итерациями

if __name__ == "__main__":
    main()
