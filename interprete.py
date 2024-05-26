import sys
import os
import descargas
import online
from player import Player
from player import Buscador
from threading import Thread
# from moduls_types import Listener
# from main import Main

## INTRODUCIR LA INSTANCIA DEL PLAYER HASTA ESTÉ CÓDIGO PARA ACCIONES COMO REPRODUCIR UNA CANCIÓN???
class Core():
    def __init__(self) -> None:
        from listener import Listener
        from main import Main
        from speaker import Speaker
        self.PATH_PLAYLISTS = 'music/playlist/'
        self.downloader = descargas.Core()
        self.online = online.Online()
        self.search_musics_links = descargas.Music_Link()
        
        self.inst_main : Main = None
        self.inst_player : Player = None
        self.inst_buscador : Buscador = None
        self.inst_listener : Listener = None
        self.inst_speaker : Speaker = None
        
        if not os.path.exists(self.PATH_PLAYLISTS):
            os.mkdir(self.PATH_PLAYLISTS)

    def set_insts(self, insts: dict = {}):
        if "inst_main" in insts:
            self.inst_main = insts["inst_main"]
        if "inst_player" in insts:
            self.inst_player = insts["inst_player"]
        if "inst_buscador" in insts:
            self.inst_buscador = insts["inst_buscador"]
        if "inst_listener" in insts:
            self.inst_listener = insts['inst_listener']
        if "inst_speaker" in insts:
            self.inst_speaker = insts["inst_speaker"]
    
    def execute(self, command=''):
        # print(f"-- Conexión a internet: {self.online.get_internet()} --")
        if any(manera == command for manera in ('salir', 'adios', 'adiós')):
            try:
                self.inst_speaker.speak("Bye")
                self.inst_main.exit()
            except Exception as e:
                print(e)
            
        elif 'mostrar' in command:
            context = command.replace('mostrar', '')
            self.mostrar(context)
        elif  any(manera in command for manera in ('reproduce','reproducir')):
            context = command.replace('reproduce', '').replace('reproducir', '').strip()
            if 'algo' in context:
                self.reproducir_playlist(context)
            elif 'bucle' in context:
                context = context.replace('en bucle', '').replace('bucle', '').strip()
                self.reproducir(context, bucle=True)
            elif context:
                self.reproducir(context)
            else:
                self.inst_speaker.speak("No puede escuchar el nombre de la canción")

        # elif 'playlist' in command:
        elif any(manera in command for manera in ('playlist', 'play list')):
            context = command.replace('playlist', '').strip()
            if any(manera in command for manera in ('numero','número')):
                num_pls = context.replace('número', '').replace('numero', '').strip()
                try:
                    num_pls = int(num_pls)
                    self.reproducir_playlist(num_pls)
                except:
                    print("|| Error al interpretar el número ||")
                    pass
            else:
                self.reproducir_playlist(context)
        elif 'siguiente' in command:
            self.inst_player.siguiente()
        elif 'anterior' in command:
            self.inst_player.anterior()
        elif any(manera in command for manera in ('bajar volúmen','bajar volumen','baja el volúmen','baja el volumen','bajar el volúmen','bajar el volumen')):
            if any(manera in command for manera in ('mínimo','minimo')):
                self.inst_player.bajar_volumen(min=True)
            else:
                self.inst_player.bajar_volumen()
        # elif ('subir volúmen' or 'subir volumen' or 'sube el volúmen' or 'sube el volumen' or 'subir el volúmen' or 'subir el volumen') in command:
        elif any(manera in command for manera in ('subir volúmen','subir volumen','sube el volúmen','sube el volumen','subir el volúmen','subir el volumen')):
            if  any(manera in command for manera in ('máximo', 'maximo')):
                self.inst_player.subir_volumen(max=True)
            else:
                self.inst_player.subir_volumen()
        elif any(manera in command for manera in ('volúmen', 'volumen')):
            command = command.replace('volúmen', '').replace('volumen', '').replace('al', '').strip()
            if any(manera in command for manera in ('mínimo', 'minimo')):
                self.inst_player.bajar_volumen(min=True)
            elif any(manera in command for manera in ('máximo', 'maximo')):
                self.inst_player.subir_volumen(max=True)
            else:
                try:
                    vol = int(command)
                    self.inst_player.establecer_volumen(vol)
                except:
                    pass
        elif any(manera in command for manera in ('pausar', 'pausa')):
            self.inst_player.pausar()
        elif any(manera in command for manera in ('reanudar', 'continuar')):
            self.inst_player.reanudar()
        elif 'repetir' in command:
            self.inst_player.repetir()
        else:
            print('|| Orden no reconocida ||')           

    
    def reproducir(self, context='', bucle=False):
        # print(f"Repro: {context} por {insts}")
        message_to_speak = ""
        music_path = ''
        resultados = self.inst_buscador.find(context)
        if len(resultados) == 0:
            print("-- Canción no encontrada --")
            message_to_speak += "Canción no encontrada. "
            # self.inst_speaker.speak("Canción no encontrada")
            if self.online.get_internet():
                print(f"-- ¿Desea descargar {context}? --")
                message_to_speak += f"¿Desea descargar {context}? "
                # self.inst_speaker.speak(message_to_speak)
                hilo = Thread(target=self.inst_speaker.speak, args=(message_to_speak,), daemon=True)
                hilo.start()
                # self.inst_speaker.speak(f"¿Desea descargar {context}?")
                # res = input("")
                res = ""
                num_rep = 5
                count = 0
                while count <= num_rep and not res:
                    print(count)
                    res = self.inst_listener.response()
                    count += 1
                    
                print("??")                    
                
                if any(manera in res for manera in ('sí', 'si')):
                    self.inst_speaker.speak("Okey, descargando la canción")
                    music_link = self.search_musics_links.search(context)
                    if music_link:
                        music_path = self.downloader.descargar(music_link, context)
        elif len(resultados) > 1:
            print(f"-- Se encontraron {len(resultados)} coincidencias --")
            message_to_speak = ""
            message_to_speak += f"Se encontraron {len(resultados)} coincidencias. "
            message_to_speak += "Artista. "
            # self.inst_speaker.add_text(f"Se encontraron {len(resultados)} coincidencias")
            # self.inst_speaker.add_text("Artista")
            print(1)
            for coincidencia in resultados:
                print(0)
                print(f" {resultados.index(coincidencia)+1}. Artista: {str(os.path.dirname(coincidencia)).split('/')[-1].title()} | Canción: {os.path.basename(coincidencia)}")
                # self.inst_speaker.add_text(f"{resultados.index(coincidencia)}. {str(os.path.dirname(coincidencia)).split('/')[-1].title()}")
                message_to_speak += f"{resultados.index(coincidencia)}. {str(os.path.dirname(coincidencia)).split('/')[-1].title()}. "
            print("-- ¿Que opción desea reproducir? --")
            # self.inst_speaker.add_text("¿Qué opción desea reproducir?")
            message_to_speak += "¿Qué opción desea reproducir?"
            # opt = input("Opción: ")
            self.inst_speaker.speak(message_to_speak)
            # thread_speaker = Thread(target=self.inst_speaker.speak, daemon=True)
            # thread_speaker.start()
            # thread_speaker.join()
            opt = ""
            num_rep = 5
            count = 0
            while count <= num_rep and not opt:
                opt = self.inst_listener.response()
            message_to_speak = ""
            if opt == 'niguna':
                print("-- Okey, cancelando reproducción --")
                # self.inst_speaker.add_text("Ok, cancelando reproducción")
                message_to_speak += "Ok, cancelando reproducción"
            else:
                try:
                    opt = "".replace("opción", "").replace("número", "").strip()
                    opt = int(opt)
                    music_path = resultados[opt-1]
                    self.inst_speaker.add_text("Okey")
                    message_to_speak += "Okey"
                except:
                    print('|| Opción no válida ||')
                    # self.inst_speaker.add_text("Opción no válida")
                    message_to_speak += "Opción no válida"
            self.inst_speaker.speak(message_to_speak)
        else:
            music_path = resultados[0]
        
        

        if music_path and bucle:
            self.inst_player.reproduce(music_path, bucle=True)
        elif music_path:
            self.inst_player.reproduce(music_path)
    
    def reproducir_playlist(self, context=''):
        if type(context) == int:
            musics_list = self.inst_buscador.make_playlist(num_pls=context)
            if musics_list:
                self.inst_player.reproduce(musics_list)
            else:
                print("|| Playlist no encontrada ||")
        elif type(context) == str:
            musics_list = []
            if context == 'algo':
                musics_list = self.inst_buscador.make_playlist(todo=True)
            else:
                musics_list = self.inst_buscador.make_playlist(artista=context)
            
            if musics_list:
                self.inst_player.reproduce(musics_list)
            else:
                print("|| Playlist no encontrada ||")



    
    def mostrar(self, context=''):
        command_valid = False
        palabras_clave = ['playlist', 'playlists', 'play list', 'play lists']
        for palabra in palabras_clave:
            if palabra in context:
                command_valid = True
        
        if command_valid:
            print()
            print('======== PLAYLISTS ========')
            print()
            list_playlists = os.listdir(self.PATH_PLAYLISTS)
            for playlist in list_playlists:
                index = list_playlists.index(playlist)
                print(f"{index} - {playlist}")
            print()


def converNum(text):
    final_text = ''
    list_num_uni = ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve']
    list_nums_dec = ['diez', 'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa']
    # nums_esp = {
    #     'once': '11','doce': '12', 'trece': '13', 'catorce': '14' 'quince': '15',
    # }

    text_split = text.replace(' ', '').split('y')
    if (len(text_split) > 1):
        final_text = f"{list_nums_dec.index(text_split[0])+1}{list_num_uni.index(text_split[1])+1}"

    print(text_split)
    print(final_text)

# converNum('ochenta y uno')
