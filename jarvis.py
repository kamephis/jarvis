import speech_recognition as sr

listener = sr.Recognizer()
command = ''

with sr.Microphone() as source:
    print("listening...")
    listener.adjust_for_ambient_noise(source=source)
    voice = listener.listen(source, timeout=3)

try:
    command = listener.recognize_google(voice)
    command = command.lower()

    if 'jarvis' in command:
        print("You said: " + listener.recognize_google(voice))

except sr.UnknownValueError:
    print(" Error")

except sr.RequestError as e:
    print("Request Error")
