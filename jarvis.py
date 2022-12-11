import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import openai
import wandb
from hueber.api import Bridge
from hueber.lib import LightBuilder


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
bridgeUser = "RA9X7Ngd5z9EVGEvZoVNa-j7D8r58zAYfxXiQ0-N"
# setup open ai
openAiSecret = "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"
openai.api_key = openAiSecret
run = wandb.init(project='GPT-3 in Python')
prediction_table = wandb.Table(columns=["prompt", "completion"])

# 4 = female computer voice (natural), 7 = jarvis
engine.setProperty('voice', voices[6].id)

hue = Bridge("192.168.178.20", bridgeUser)

LightsMapper = {
    "light": 8,
    "fitness": 2
}


# just for debugging the hue lights
# print(hue.groups)
# print(hue.lights)


def switch_device(key):
    if key in LightsMapper:
        is_on = hue.lights[LightsMapper[key]].data['state']['on']

        new_update = LightBuilder()
        new_update["on"] = not is_on
        new_update["bri"] = 254
        hue.lights[LightsMapper[key]].push(new_update.update_str())


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:

            listener.adjust_for_ambient_noise(source=source)
            voice = listener.listen(source, timeout=4)

            command = listener.recognize_google(voice)
            command = command.lower()

            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                print(command)

            talk(command)

    except sr.UnknownValueError:
        pass
        print(" Error")

    except sr.RequestError as e:
        print("Request Error")
        pass
    return command


def run_jarvis():
    print("listening...")
    talk('How may I serve you?')
    command = take_command()
    print(command)
    # print(hue.lights);

    if 'turn on light' in command:
        device = command.replace('turn on ', '')
        switch_device(device)

    elif 'turn off light' in command:
        device = command.replace('turn off ', '')
        switch_device(device)

    elif 'hello' in command:
        device = command.replace('ask' , '')
        
        # test the ai
        #gpt_prompt = "Correct this to standard English:\n\nShe no went to the market."
        print('ask your question')
        #command()
        gpt_prompt = 'She no go market'

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=gpt_prompt,
            temperature=0.5,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        print(response['choices'][0]['text'])
        prediction_table.add_data(gpt_prompt, response['choices'][0]['text'])
        wandb.log({'predictions': prediction_table})
        wandb.finish()
        talk(response['choices'][0]['text'])

    elif 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)

    elif 'who is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    elif 'date' in command:
        talk('sorry, I have a headache')

    elif 'are you single' in command:
        talk('I am in a relationship with wifi')

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    else:
        talk('I am sorry, please speak your command')

while True:
    run_jarvis()
