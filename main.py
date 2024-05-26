import sys
import time
import threading

import eventos
import player
import interprete
import listener
import speaker
# import interfaz

class Main():
    def __init__(self) -> None:
        self.ejecucion = True
    
    def exit(self):
        self.ejecucion = False

    def get_ejecucion(self):
        return self.ejecucion





if __name__ == '__main__':
#    inst_interfaz = interfaz.Demo()
#    inst_interfaz.fps_monitor_start()
    inst_main = Main()
    inst_player = player.Player()
    inst_buscador = player.Buscador()
    inst_interprete = interprete.Core()
    inst_listener = listener.Listener()
    inst_speaker = speaker.Speaker()
    
    instancias = {
        'inst_main': inst_main,
        'inst_interprete': inst_interprete,
        'inst_player': inst_player, 
        'inst_buscador': inst_buscador,
        'inst_listener': inst_listener,
        'inst_speaker': inst_speaker
 #       'inst_interfaz': inst_interfaz
    }
    
    inst_listener.set_insts(instancias)
    inst_interprete.set_insts(instancias)
    
    
    hilo_recivir_ordenes = threading.Thread(target=eventos.recivir_orden, args=(inst_listener,), daemon=True)

    hilo_recivir_ordenes.start()
    
    # inst_speaker.add_text("Hola, soy Max, llamame si necesitas ayuda")
    # inst_speaker.add_text("xd")
    # inst_speaker.add_text("Hola, soy Max, llamame si necesitas ayuda")
    
    inst_speaker.speak("Hola, soy Max, llamame si necesitas ayuda")

    while inst_main.get_ejecucion():
        time.sleep(10)

#    inst_interfaz.run()
    # print('holas')
    # inst_interfaz.on_stop()