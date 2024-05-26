import os
import time
import threading
import pyperclip
from pytube import YouTube, Playlist

import conversor
import online

class Core():
    def __init__(self) -> None:
        self.PATH_MP4 = 'music/mp4/'
        self.conversor = conversor.Core()

    def descargar(self, link='', music_name=''):
        if not os.path.exists(self.PATH_MP4):
            os.mkdir(self.PATH_MP4)
        
        if not 'playlist' in link:
            try:

                yt = YouTube(link)

                author = yt.author.lower().replace(' ','')
                title = ''
                if music_name:
                    title = music_name
                else:
                    title = yt.title.lower()
                
                
                limit = 100
                cont = 0
                descarga_completa = False
                while not descarga_completa and cont < limit:
                    try:
                        print(f"-- Titulo: {title} --")

                        vid_path = yt.streams.get_highest_resolution().download(self.PATH_MP4)
                        # vid_path = yt.streams.get_audio_only().download(self.PATH_MP4)
                        print(f"PATH: {vid_path}")
                        print(f'FILE NAME: {os.path.basename(vid_path)}')
                        descarga_completa = True
                        print('-- Descarga Completa --')
                    except:
                        
                        print(f"|| Error con la descarga, intento N° {cont} ||")
                    cont += 1
                
                music_path, conversion_completa = self.conversor.convertir(vid_path=vid_path, playlist_name=author)

                if conversion_completa:
                    print("-- Conversión completa --")
                else:
                    print("|| Error en la conversión ||")
                
                return music_path
                
            except:
                print('|| Error al descargar la canción ||')
        
        else:
            try:
                if not os.path.exists(f"{self.PATH_MP4}/newpls/"):
                    os.mkdir(f"{self.PATH_MP4}/newpls/")
                
                playlist = Playlist(link)

                try:
                    for video in playlist:
                        yt = YouTube(video)
                        author = yt.author.lower().replace(' ','')
                        limit = 50
                        cont = 0
                        descarga_completa = False
                        while not descarga_completa and cont < limit:
                            try:
                                print(f"-- Titulo: {yt.title} --")
                                
                                vid_path = yt.streams.get_highest_resolution().download(f"{self.PATH_MP4}/newpls/")

                                # vid_path = yt.streams.get_lowest_resolution().
                                descarga_completa = True
                                print('-- Descarga Completa --')
                            except:
                                print(f"|| Error con la descarga, intento N° {cont} ||")
                            cont += 1

                        music_path, conversion_completa = self.conversor.convertir(vid_path=vid_path, playlist_name=author)

                        if conversion_completa:
                            print(f"PATH: {music_path} | Conversión completa")
                        else:
                            print(f"PATH: {music_path} | Error de conversión")

                    print('-- Playlist descargada con éxito --')
                except:
                    print('|| Error al descargar la playlist ||')
            except:
                print('|| Error al descargar la playlist ||')


class Music_Link():
    def __init__(self) -> None:
        self.lib_imported = False
        self.online = online.Online(unit=True)
    
    def search(self, music_name='') -> str:
        if self.online.get_internet():
            try:
                import pywhatkit
                link = pywhatkit.playonyt(music_name, open_video=False)
                # self.online.stop()
                return link
            except Exception as e:
                print(e)
            


# descargador = Core()

# link = 'https://www.youtube.com/watch?v=QlZNGcVfeF0&pp=ygUIY29sdW1iaWE%3D'
# link = 'https://www.youtube.com/playlist?list=PLsIzLTThWwu3A_nt1Iz13SIOF4g41BoYe'
# music_name = 'columbia'
# print(f"FUNCION DESCARGA | RETURN: {descargador.descargar(link)}")