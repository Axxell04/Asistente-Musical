import os
import random
import threading
import time

import pygame
from pygame import mixer

# playlist_musicactual = {}
# index_music = 0

PATH_MUSIC = 'music/'
PATH_MP4 = 'music/mp4/'
PATH_PLAYLISTS = 'music/playlist/'

# MUSIC_END_PLAYLIST = pygame.USEREVENT+1
# MUSIC_END_ALGO = pygame.USEREVENT+2
# evento_actual = 0

# pygame.init()
# mixer.init()

# mixer.music.set_volume(0.5714)

class Player():
    def __init__(self) -> None:
        pygame.init()
        mixer.init()
    
        mixer.music.set_volume(0.5)
        self.vol_act = mixer.music.get_volume()
        self.intervalo_volumen = 0.1

        self.PATH_MUSIC = 'music/'
        self.PATH_MP4 = 'music/mp4/'
        self.PATH_PLAYLISTS = 'music/playlist/'
        if not os.path.exists(self.PATH_MUSIC):
            os.mkdir(self.PATH_MUSIC)
            os.mkdir(self.PATH_MUSIC)

        self.MUSIC_END_PLAYLIST = pygame.USEREVENT+1
        self.MUISC_END_BUCLE = pygame.USEREVENT+2
        # self.MUSIC_END_ALGO = pygame.USEREVENT+2
        self.evento_actual = 0

        # self.effect_active = mixer.Sound('effects/active.mp3')
        # self.effect_desactive = mixer.Sound('effects/desactive.mp3')
        # self.effect_key = mixer.Sound('effects/palabraclave.mp3')
        self.effects = {
            'active': mixer.Sound('effects/active.mp3'),
            'desactive': mixer.Sound('effects/desactive.mp3'),
            'key': mixer.Sound('effects/palabraclave.mp3')
        }

        self.musics_list = []
        self.index_music = 0
        self.ultima_reproduccion = ''
        self.bucle = False

        self.hilo_revision_eventos = threading.Thread(target=self.revision_eventos, daemon=True)
        self.hilo_revision_eventos.start()
    
    def play_effect(self, name):
        try:
            self.effects[name].play()
        except:
            print('|| Efecto no encontrado ||')
    
    def reproduce(self, content='', bucle=False):
        """Recibe el path de una canción o una lista de paths"""
        self.index_music = 0
        self.bucle = False

        if content:
            if type(content) == str:
                mixer.music.load(content)
                mixer.music.play()
                if bucle:
                    self.bucle = True
                    self.evento_actual = self.MUISC_END_BUCLE
                    mixer.music.set_endevent(self.evento_actual)
                else:
                    self.evento_actual = 0
                    mixer.music.set_endevent()

                self.ultima_reproduccion = content
                self.musics_list.clear()
            elif type(content) == list:
                self.musics_list = content
                mixer.music.load(self.musics_list[self.index_music])
                mixer.music.play()
                mixer.music.set_endevent(self.MUSIC_END_PLAYLIST)
                self.ultima_reproduccion = self.musics_list[self.index_music]
                self.evento_actual = self.MUSIC_END_PLAYLIST
    
    def revision_eventos(self):
        while True:
            time.sleep(1)
            if (self.evento_actual != 0) and (mixer.music.get_pos() == -1):
                if self.evento_actual == self.MUSIC_END_PLAYLIST:
                    print("Siguiente Canción")
                    self.siguiente()
                if self.evento_actual == self.MUISC_END_BUCLE:
                    print("-- Repitiendo --")
                    self.repetir()

    def siguiente(self):
        if len(self.musics_list) <= 1:
            self.evento_actual = 0
            mixer.music.set_endevent()
            return
        
        if self.index_music == len(self.musics_list)-1:
            self.musics_list.reverse()
            self.index_music = 0
        
        self.index_music += 1

        mixer.music.load(self.musics_list[self.index_music])
        mixer.music.play()
        self.ultima_reproduccion = self.musics_list[self.index_music]
    
    def anterior(self):
        if self.index_music == 0:
            self.musics_list.reverse()
            self.index_music = 1
        
        self.index_music -= 1

        mixer.music.load(self.musics_list[self.index_music])
        mixer.music.play()
        self.ultima_reproduccion = self.musics_list[self.index_music]
    
    def pausar(self):
        try:
            mixer.music.set_endevent()
            mixer.music.pause()
            print('-- Canción pausada --')
            mixer.music.set_endevent(self.evento_actual)
        except:
            print('|| Sin canción reproduciendo ||')
    
    def reanudar(self):
        try:
            mixer.music.unpause()
        except:
            print("|| Sin canción en pausa ||")
    
    def repetir(self):
        if mixer.music.get_busy():
            mixer.music.set_pos(0.0)
        elif self.ultima_reproduccion and self.bucle:
            self.reproduce(self.ultima_reproduccion, bucle=True)
        elif self.ultima_reproduccion:
            self.reproduce(self.ultima_reproduccion)
        else:
            print('|| Sin canción reproduciendo ||')

    def bajar_volumen(self, min=False):
        if self.vol_act <= 0.1:
            print("|| Volúmen al mínimo ||")
            return

        if min:
            self.establecer_volumen(0.1)
            
        else:
            vol = round(self.vol_act-self.intervalo_volumen, 1)
            self.establecer_volumen(vol)

    def subir_volumen(self, max=False):
        if self.vol_act >= 1:
            print("|| Volúmen al máximo ||")
            return

        if max:
            self.establecer_volumen(1.0)
        else:
            vol = round(self.vol_act+self.intervalo_volumen, 1)
            self.establecer_volumen(vol)
    
    def establecer_volumen(self, vol=0):
        if vol:
            if type(vol) == int:
                vol = vol/10
            
            vol = round(vol, 1)
            if vol >= 0.1 and vol <= 1:
                self.vol_act = vol
                mixer.music.set_volume(self.vol_act)
                print(f"VOLUMEN ACTUAL: {self.vol_act} {type(self.vol_act)}")


        



class Buscador():
    def __init__(self) -> None:
        self.PATH_PLAYLISTS = PATH_PLAYLISTS

    def find(self, music_name):
        music_path = ''
        resultados = []
        for playlist in os.listdir(self.PATH_PLAYLISTS):
            for music in os.listdir(f"{self.PATH_PLAYLISTS}/{playlist}"):
                if music_name in music:
                    index_coincidencia = music.find(music_name)
                    if ord(music[index_coincidencia-1]) not in range(65,90) and ord(music[index_coincidencia-1]) not in range(97,122):
                        music_path = f"{self.PATH_PLAYLISTS}/{playlist}/{music}"

                        resultados.append(music_path)
                        # return music_path
        
        return resultados

    def make_playlist(self, todo=False, artista='', num_pls=-1):
        musics_list = []
        if todo:
            for playlist in os.listdir(self.PATH_PLAYLISTS):
                for music_name in os.listdir(f"{self.PATH_PLAYLISTS}/{playlist}"):
                    music_path = f"{self.PATH_PLAYLISTS}/{playlist}/{music_name}"

                    musics_list.append(music_path)
        
            musics_list = self.random_list(musics_list)
            return musics_list
        
        elif num_pls != -1:
            list_playlists = os.listdir(self.PATH_PLAYLISTS)

            for playlist in list_playlists:
                index = list_playlists.index(playlist)

                if index == num_pls:
                    for music_name in os.listdir(f"{self.PATH_PLAYLISTS}/{playlist}"):
                        music_path = f"{self.PATH_PLAYLISTS}/{playlist}/{music_name}"

                        musics_list.append(music_path)
            
            musics_list = self.random_list(musics_list)
            return musics_list

        elif artista:
            playlist_name = ''
            for playlist in os.listdir(self.PATH_PLAYLISTS):
                if artista in playlist:
                    playlist_name = playlist
            
            if not playlist_name:
                list_playlists = os.listdir(self.PATH_PLAYLISTS)
                for playlist in list_playlists:
                    num_letras = len(playlist)
                    coincidencias = 0
                    playlist_mod = playlist
                    for letra in list(artista):
                        if letra in playlist_mod:
                            coincidencias += 1
                            playlist_mod = playlist_mod.replace(letra, '', 1)

                    if coincidencias >= ((num_letras * 70) / 100):
                        playlist_name = playlist
            
            if playlist_name:
                for music_name in os.listdir(f"{self.PATH_PLAYLISTS}/{playlist_name}"):
                    music_path = f"{self.PATH_PLAYLISTS}/{playlist_name}/{music_name}"

                    musics_list.append(music_path)
            
            musics_list = self.random_list(musics_list)
            return musics_list



    

    def random_list(self, init_list):
        final_list = []
        index_agregados = []
        index = 0

        for i in init_list:
            while True:
                index = random.randint(a=0,b=len(init_list)-1)
                if index_agregados.__contains__(index):
                    pass
                else:
                    index_agregados.append(index)
                    break
            final_list.append(init_list[index])

        return final_list

