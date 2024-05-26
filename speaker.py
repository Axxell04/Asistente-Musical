import json
import pyttsx3
from queue import Queue

class Speaker():
    def __init__(self) -> None:
        self.config = {}
        with open("config.txt", "r") as file:
            self.config = json.loads(file.read())
        
        self.engine = pyttsx3.init()
    
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[0].id)
        self.engine.setProperty("rate", self.config["velocidad"])
        self.engine.setProperty("volume", self.config["volumen"])
        
        self.queue_text = Queue()
        # self.engine.runAndWait()
    
    def add_text(self, text):
        self.queue_text.put(text)
    
    def speak(self, text):
        self.engine.say(text)
        try:
            self.engine.runAndWait()
        except:
            pass