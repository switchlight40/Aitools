import ollama
import elevenlabs
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import speech_recognition as sr
import json
import requests
import pyaudio
class Ai():

    #ElevenLabs settings
    ElevenLabs_Apikey = None
    voice = ''

    #ollama settings
    model = ''
    messages = []
    
    #misc variables
    srdelay = 3 #delay is how long the stt function should go on for per cycle (how long to listen for)
    addressraw = "" #Mainly for if you want to run ollama as server so just use the chatraw and set this variable to your ipadress and whatever port you set in env variables


    #Private variables
    _fulltext = ""
    _voicesettings = elevenlabs.VoiceSettings(stability=0.5,similarity_boost=0.75,style=0.3,use_speaker_boost=True)


    def __init__(self,model):
        self.model = model


#Ollama related functions

    def generate(self,prompt):
        return ollama.generate(self,prompt)

    def chat(self,prompt):
        try:
            self.messages.append({
                'role': 'user',
                'content': prompt,
            })

            response: ollama.ChatResponse = ollama.chat(model=self.model,
                                                        messages=self.messages)
            
            return response.message.content
        except Exception as e:
            return f":/ An error has occoured: {e}"
        
    def clearcontext(self):
        self.messages = []
        return True


#Ollama related RAW functions        
    def generateraw(self,prompt,stream: bool = False):
        data = {
            "model": self.model,
            "stream": stream,
            "prompt": prompt

        }
        url = self.addressraw + "/api/generate"
        response = requests.post(url,json=data)
        pyresponse = json.loads(response.text)
        return pyresponse["response"]
        
        
    def chatraw(self,prompt,stream: bool = False):
        self.messages.append({
                'role': 'user',
                'content': prompt,
            })
        data = {
            "model": self.model,
            "stream": stream,
            "messages": self.messages
        }
        url = self.addressraw + "/api/chat"
        response = requests.post(url,json=data)
        pyresponse = json.loads(response.text)
        content = pyresponse["message"]["content"]
        return content
        

#ElevenLabs related functions

    def tts(self,text):
        client = ElevenLabs(api_key=self.ElevenLabs_Apikey)
        
        audio = client.generate(

            text=str(text),
            voice=self.voice,
            model="eleven_flash_v2_5",
            voice_settings=self._voicesettings

        )

        return audio
    
    def voicesetting(self,stablility: float,style: float,speakerboost: bool):
        self._voicesettings = elevenlabs.VoiceSettings(stability=stablility,
                                                      style=style,
                                                      use_speaker_boost=speakerboost)
        
        return True

    def playaudio(audio,ffmpeg = True):
        play(audio,use_ffmpeg=ffmpeg)

#Speach recognition functions
    def stt(self,text):
        with sr.Microphone as source:
            r = sr.Recognizer
            audio_data = r.record(source, duration=self.srdelay)
            try:
                text = r.recognize_google(audio_data)
                self._fulltext = self._fulltext + " " + text
            except:
                return False
        return True

    def clearfulltext(self):
        self._fulltext = ""
        return True

