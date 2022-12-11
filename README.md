# for m1 mac
run: 
`LDFLAGS="-L$(brew --prefix portaudio)/lib" CFLAGS="-I$(brew --prefix portaudio)/include" python3 -m pip install pyaudio`

and then: 
`python3 -m pip install -r requirements.txt`

## Requirements
SpeechRecognition
pyttsx3
PyAudio
pywhatkit
wikipedia
pyjokes
hueber