import speech_recognition as sr
import json
import time
import threading
import queue
import asyncio
import websockets
from pynput import keyboard

from player import Player, Buscador

import vosk
import pyaudio

class Listener():
    def __init__(self) -> None:
        from interprete import Core
        self.tiempo_transcurrido = 0
        self.player = Player()

        self.CHANNELS = 1
        self.FRAME_RATE = 16000
        self.REC_SEC = 16
        self.AUDIO_FORMAT = pyaudio.paInt16
        self.SAMPLE_SIZE = 2
        self.recordings = queue.Queue()
        self.micro_on = queue.Queue()
        
        #VOSK
        self.model = vosk.Model(model_name="vosk-model-small-es-0.42")
        self.recognizer = vosk.KaldiRecognizer(self.model, self.FRAME_RATE)
        self.recognizer.SetWords(True)
        
        #SPEECH_RECOGNITION
        self.recognizer_sr_hotword = sr.Recognizer()
        self.recognizer_sr_command = sr.Recognizer()
        self.recognizer_sr_res = sr.Recognizer()
        self.microphone_sr = sr.Microphone()
        
        # with self.microphone_sr as source:
        #     self.recognizer_sr.adjust_for_ambient_noise(source)
        
        self.KEYWORD = "max"
        self.inst_interprete : Core = None
        self.inst_player : Player = None
        self.inst_buscador : Buscador = None
    
    def set_insts(self, insts: dict = {}):
        if "inst_interprete" in insts:
            self.inst_interprete = insts["inst_interprete"]
        if "inst_player" in insts:
            self.inst_player = insts["inst_player"]
        if "inst_buscador" in insts:
            self.inst_buscador = insts["inst_buscador"]
        
    def close_micro(self):
        if not self.micro_on.empty():
            self.micro_on.get()
    
    def open_micro(self):
        if self.micro_on.empty():
            self.micro_on.put(True)
    
            
    async def run_listening_server(self):
        async with websockets.serve(self.reciv_wireless, "", 8888):
            await asyncio.Future()
    
    
    
    def start(self):
        thread_server = threading.Thread(target=asyncio.run, args=(self.run_listening_server(),), daemon=True)
        thread_server.start()
            
    async def reciv_wireless(self, websocket):
        print("Conexión establecida")
        while True:
            data = await websocket.recv()
            if data:
                thr_wir_trans = threading.Thread(target=self.wireless_transcript, args=(data,), daemon=True)
                thr_wir_trans.start()
    
    def wireless_transcript(self, data):
        try:
            recognizer = vosk.KaldiRecognizer(self.model, self.FRAME_RATE)
            recognizer.SetWords(True)
            
            recognizer.AcceptWaveform(data)
            result = recognizer.Result()
            text = json.loads(result)["text"]
            if text:
                print(text)
                if self.KEYWORD in text:
                    orden = text.replace(self.KEYWORD, "").strip()
                    self.inst_interprete.execute(command=orden, insts={'player': self.inst_player, 'buscador': self.inst_buscador})
        except Exception as e:
            print(e)

    def record_microphone(self, chunk=1024):
        p = pyaudio.PyAudio()
        
        stream = p.open(rate=self.FRAME_RATE, channels=self.CHANNELS, format=self.AUDIO_FORMAT, input=True, frames_per_buffer=chunk)
        
        frames = []
        
        while not self.micro_on.empty():
            data = stream.read(chunk)
            frames.append(data)
            if len(frames) >= (self.FRAME_RATE * self.REC_SEC) / chunk:
                self.recordings.put(frames.copy())
                frames = []
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    def speech_recognition(self, inst_interprete, inst_player, inst_buscador): 
        while not self.micro_on.empty():
            frames = self.recordings.get()
            
            self.recognizer.AcceptWaveform(b''.join(frames))
            result = self.recognizer.Result()
            text = json.loads(result)["text"]
            if text:
                print(text)
                if self.KEYWORD in text:
                    orden = text.replace(self.KEYWORD, "").strip()
                    inst_interprete.execute(command=orden, insts={'player': inst_player, 'buscador': inst_buscador})
    
    def listen(self):
        with sr.Microphone() as source:
            self.player.play_effect('active')
            print("Escuchando...")
            voice = self.recognizer_sr_command.listen(source, phrase_time_limit=6, timeout=5)
            text = self.recognizer_sr_command.recognize_google(voice, language="es-ES")
            # rec = self.recognizer.recognize_vosk(voice, 'es')
            # rec = rec.lower().replace('{', '').replace('}', '').replace('"', '').replace('text', '').replace(':', '').strip()
            
            text = text.lower().strip()
            
            print(text)
            self.inst_interprete.execute(command=text)
    
    def response(self) -> str:
        res = ""
        with sr.Microphone() as source:
            # self.player.play_effect('active')
            try:
                voice = self.recognizer_sr_res.listen(source, phrase_time_limit=4, timeout=3)
                text = self.recognizer_sr_res.recognize_google(voice, language="es-ES")
                res = text.lower().strip()
            except:
                pass
        
        print(res)
        return res
    
    def listener_loop(self):
        with self.microphone_sr as source:
            while True:
                try:
                    voice = self.recognizer_sr_hotword.listen(source, timeout=7, phrase_time_limit=4)
                    text = self.recognizer_sr_hotword.recognize_google(voice, language="es-ES") 
                    text = text.lower().strip()
                    if self.KEYWORD in text:
                        thread_command = threading.Thread(target=self.listen, daemon=True)
                        thread_command.start()
                        
                except Exception as e:
                    pass
                # time.sleep(1)
                    
    def start_listener(self):
        thread_lis_loop = threading.Thread(target=self.listener_loop, daemon=True)
        thread_lis_loop.start()
    
    def on_press(self, key):
        if key == keyboard.Key.alt_l:
            momento = time.time()
            self.tiempo_transcurrido += momento
            if self.tiempo_transcurrido > (momento * 15):
                self.tiempo_transcurrido = 0
                return False
    
    def listen_key(self):
        try:
            with keyboard.Listener(on_press=self.on_press) as listenerkey:
                listenerkey.join()
            print("Hola")
            return self.listen()
        except:
            pass
    
    def toggle_listen(self, inst_interprete, inst_player, inst_buscador):
        try:
            with keyboard.Listener(on_press=self.on_press) as listenerkey:
                listenerkey.join()
            
            if self.micro_on.empty():
                inst = {
                    'inst_interprete': inst_interprete,
                    'inst_player': inst_player,
                    'inst_buscador': inst_buscador
                }
                self.open_micro()
                record = threading.Thread(target=self.record_microphone, daemon=True)
                record.start()
                transcript = threading.Thread(target=self.speech_recognition, kwargs=inst, daemon=True)
                transcript.start()
                print("Escuchando..")
            else:
                self.close_micro()
                print("Se dejó de escuchar..")
        except Exception as e:
            print(e)

