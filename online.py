import signal
import time
import requests
import threading
import os


class Online ():
    def __init__(self, unit=False) -> None:
        self.unit = unit
        self.internet = False
        try:
            request = requests.get("https://www.google.com", timeout=5)
            self.internet = True
        except:
            self.internet = False

        print(f"CONNECTION: {self.internet}")

        if not self.unit:
            self.hilo_revisión = threading.Thread(target=self.check_connection, daemon=True)
            
            self.hilo_revisión.start()


    def get_internet(self):
        if not self.unit:
            return self.internet
        else:
            try:
                request = requests.get("https://www.google.com", timeout=5)
                self.internet = True
            except:
                self.internet = False
            return self.internet

        

    def stop(self):
        os.kill(self.hilo_revisión.ident, signal.SIGINT)


    def check_connection(self):
        while True:
            try:
                request = requests.get("https://www.google.com", timeout=5)
                self.internet = True
            except:
                self.internet = False
            finally:
                # print(f"CONNECTION: {self.internet}")
                pass
            time.sleep(60)


# online = Online()

# while True:
#     try:
#         time.sleep(.2)
#         print(online.internet)
#     except:
#         print("-- Ejecución terminada --")
#         break