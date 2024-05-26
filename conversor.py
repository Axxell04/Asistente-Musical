import os
import shutil
# from moviepy.video.io.VideoFileClip import VideoFileClip
import ffmpeg


class Core():
    def __init__(self) -> None:
        self.PATH_MP4 = 'music/mp4/'
        self.PATH_PLAYLISTS = 'music/playlist/'
    
    def convertir(self, vid_path = '', list_vids_path = [], playlist_name = 'ABC'):
        if vid_path:
            target_dir = os.path.join(self.PATH_PLAYLISTS, playlist_name)
            if os.path.exists(target_dir):
                pass
            else:
                nombre_asociado = self.playlists_asociadas(playlist_name)
                if nombre_asociado:
                    list_dirs_eliminar = self.unir_playlists(nombre_asociado)
                    for dir in list_dirs_eliminar:
                        shutil.rmtree(dir)
                    target_dir = os.path.join(self.PATH_PLAYLISTS, nombre_asociado)
                else:
                    os.mkdir(target_dir)
        
        vid_name = os.path.basename(vid_path).replace('mp4', 'mp3').lower()
        caracteres_prohibidos = ['\\','/',':','*','?','"','<','>','|']
        for caracter in caracteres_prohibidos:
            if caracter in vid_name:
                vid_name = vid_name.replace(caracter, '')
        
        music_path = os.path.join(target_dir, vid_name)
        abs_music_path = os.path.abspath(music_path)
        print(abs_music_path)

        # clip = VideoFileClip(vid_path)
        conversion_completa = False
        try:
            ffmpeg_path = 'ffmpeg/ffmpeg.exe'
            stream = ffmpeg.input(vid_path)
            stream = ffmpeg.output(stream, music_path)
            ffmpeg.run(stream, cmd=ffmpeg_path, overwrite_output=True)
            conversion_completa = True
        except Exception as e:
            print(e)
            pass

        # clip.close()

        try:
            shutil.rmtree(self.PATH_MP4)
        except:
            pass
        
        return music_path, conversion_completa
    

    def playlists_asociadas(self, playlist_name=''):
        playlist_A = playlist_name
        artista = ''
        for playlist in os.listdir(self.PATH_PLAYLISTS):
            playlist_B = playlist
            letras_playlist_A = list(playlist_A)
            letras_playlist_B = list(playlist_B)
            index_letra = 0
            coincidencias = 0
            coincidencias_txt = ''
            if playlist_A != playlist_B:
                for letra in letras_playlist_A:
                    try:
                        if letra == letras_playlist_B[index_letra]:
                            coincidencias += 1
                            coincidencias_txt += letra
                    except:
                        pass
                    index_letra += 1

                if coincidencias > 4:
                    artista = coincidencias_txt
        return artista
    
    def unir_playlists(self, artista = ''):
        if artista:
            list_dirs_eliminar = []
            artista_path = os.path.join(self.PATH_PLAYLISTS, artista)
            if not os.path.exists(artista_path):
                os.mkdir(artista_path)
            
            for playlist in os.listdir(self.PATH_PLAYLISTS):
                if artista != playlist:
                    if artista in playlist:
                        playlist_asociada_path = os.path.join(self.PATH_PLAYLISTS, playlist)
                        musics_playlist_asociada = os.listdir(playlist_asociada_path)
                        for music in musics_playlist_asociada:
                            path_origen = os.path.join(playlist_asociada_path, music)
                            path_destino = os.path.join(artista_path, music)

                            if not os.path.exists(path_destino):
                                shutil.copy2(path_origen, path_destino)
                        
                        list_dirs_eliminar.append(playlist_asociada_path)
            
            return list_dirs_eliminar


