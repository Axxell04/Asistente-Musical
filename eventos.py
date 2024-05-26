import os

def send_messages(instancia):
    # instancia.change_comand_mode(message)
    while True:
        message = input('Message: ')
        instancia.agregar_registro(contenido=message)

def reproducir(instancia_player, instancia_buscador):
    while True:
        cancion = input('Ingrese el nombre de la canción: ')
        # instancia.reproduce(modo='unico', cancion=cancion)
        music_path = instancia_buscador.find(cancion)
        if music_path:
            instancia_player.reproduce(music_path)
        else:
            print("-- CANCION NO ENCONTRADA --")

def imprimir(x):
    print(f'---- {x}')

def playlist(inst_player, inst_buscador):
    while True:
        artista = input("Artista: ")
        musics_paths_list = inst_buscador.make_playlist(artista=artista)
        
        print(*musics_paths_list, sep="\n")
        inst_player.reproduce(musics_paths_list)

def recivir_orden(inst_listener=''):
    inst_listener.start_listener()
    while True:
        orden = inst_listener.listen_key()
