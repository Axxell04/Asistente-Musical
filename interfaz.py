import threading
import gc

from kivy.clock import mainthread
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen, MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.controllers import WindowController
from kivymd.icon_definitions import md_icons


class MyScreen(Screen, WindowController):
    # def on_width(self, *args):
    #     print(self.width)
    
    def on_size(self, *args):
        # print(self.size)
        pass
        Demo.actualizar(self_Demo,self_Demo,self.size)
print('XD')
num = 0
self_Demo = ''
ultimo_reg = ''
class Demo(MDApp):
    @mainthread
    def actualizar(self,obj,size):
        if size[0] < 270 or size[1] < 350:
            self.contenedor_registro.opacity = 0
            if size[0] < 270:
                # self.btn_borrar.pos_hint = {'center_x': 0.5, 'center_y': .2}
                self.btn.pos_hint = {'center_x': 0.5, 'center_y': .3}
                self.btn_ejecutar.pos_hint = {'center_x': 0.5, 'center_y': .1}
                self.comandos_field.width = '100px'
            if size[1] < 350:
                self.btn.pos_hint={'center_x': 0.5, 'center_y': .5}  
                self.comandos_field.pos_hint = {'center_x': 0.5, 'center_y': .78}  
        else:
            self.contenedor_registro.opacity = 1
            if size[0] > 270:
                # self.btn_borrar.pos_hint = {'center_x': 0.4, 'center_y': .1}
                self.btn.pos_hint = {'center_x': 0.5, 'center_y': .2}
                self.btn_ejecutar.pos_hint = {'center_x': 0.5, 'center_y': .1}
                self.comandos_field.width = '270px'
            if size[1] > 350:
                self.btn.pos_hint={'center_x': 0.5, 'center_y': .2}
                self.comandos_field.pos_hint = {'center_x': 0.5, 'center_y': .4} 
        
        for elemento in self.lista_registro.children:
            # print(elemento.size)
            # elemento.size_hint = (self.contenedor_registro.width, "20px"),
            elemento.width = self.contenedor_registro.width
        
        # if size[1] < 350:
        #     self.contenedor_registro.opacity = 0
        #     self.btn.pos_hint={'center_x': 0.5, 'center_y': .5}
        # else:
        #     self.contenedor_registro.opacity = 1
        #     self.btn.pos_hint={'center_x': 0.5, 'center_y': .2}
        
        # self.screen.remove_widget(self.contenedor_registro)
            

    def build(self):
        global self_Demo, cuadro_comandos_visible, demo_exist, conexion_internet
        # global self_Demo
        self_Demo = self
        demo_exist = True
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Cyan'
        screen = MyScreen()
        # screen
        # print(screen.get_parent_window())
        self.screen = screen
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_key_down)
        print(self.keyboard)

        # lbl = MDLabel(text='Hola Mundo', halign='center', theme_text_color='Custom', text_color=(0.5, 0, 0.5, 1), font_style='Caption')
        # lbl2 = MDLabel(text='LBL 2', pos_hint={'center_x': 0.5, 'center_y': 0.6}, theme_text_color='Custom', text_color=(0.5, 0, 0.5, 1), font_style='Caption')
        self.btn = MDIconButton(
            text='LLAMAR', pos_hint={'center_x': 0.5, 'center_y': .2},
            on_release=self.btnfunc, icon="microphone", theme_text_color="Custom",
            icon_size='50px', icon_color='cyan'
            )
        # self.btn.line
        self.comandos_field = MDTextField(text='', size_hint_x=None, width=250, pos_hint = {'center_x': 0.5, 'center_y': .6})
        # self.comandos_field.opacity = 0
        self.comandos_field.focus = True
        self.btn_ejecutar = MDRectangleFlatButton(text='Ejecutar', pos_hint={'center_x': .6, 'center_y':.1}, on_release=self.ejecutar_comando)

        # if not conexion_internet:
        #     self.comandos_field.opacity = 1
        #     self.btn_ejecutar.opacity = 1
        #     cuadro_comandos_visible = True
        # else:
        #     self.comandos_field.opacity = 0
        #     self.btn_ejecutar.opacity = 0
        #     cuadro_comandos_visible = False
        
        # self.comandos_field.multiline = True
        self.comandos_field.hint_text = 'Insertar comando'
        
        # self.comandos_field.
        # self.link_field.select_all()
        # self.link_field.delete_selection()
        # self.link_field.focus = True
        # self.link_field.paste()
        # print(md_icons['language-python'])
        # iconos = list(md_icons.items())
        # self.btn_borrar = MDIconButton(
        #     icon='clipboard-remove-outline',
        #     pos_hint = {'center_x': 0.4, 'center_y': .1},
        #     icon_size='30px'
        # )
        self.contenedor_registro = MDScrollView(pos_hint={'center_x': 0.5, 'center_y': 0.65}, size_hint_x=.8, size_hint_y=.6,
            line_color='cyan', line_width='3px', scroll_timeout=10000, scroll_distance=2, do_scroll_x=True, bar_width=10, 
            scroll_type=['bars','content'], scroll_wheel_distance=70, smooth_scroll_end=20)
        
        self.lista_registro = MDList (            
            id='box',
            adaptive_size=True,
            spacing='20px',
            
            # size_hint_x = .3,
            pos_hint={
                'center_x': .5, 'center_y':.5
            },
            # md_bg_color = 'blue'
            )
        # self.lista_registro.
        self.contenedor_registro.add_widget(self.lista_registro)

        # self.registro.size_hint_x = .5
        # self.registro.size_hint_y = .5
        self.lista_registro.adaptive_height = True
        self.lista_registro.adaptive_width =True  

        

        lista_elementos = [ self.btn, self.contenedor_registro, self.comandos_field, self.btn_ejecutar]

        for elemento in lista_elementos:
            screen.add_widget(elemento)

        

        return screen
    
    def change_comand_mode(self, message):
        print('Mode change: ', message)
    
    # @mainthread
    def keyboard_closed(self):
        print('My keyboard have been closed!')
        pass

    # @mainthread
    def on_key_down(self, keyboard, keycode, text, modifiers):
        # print(self.comandos_field.focus)
        if keycode[1] == 'enter' and self.comandos_field.text != '':
            print(f"Ejecutando comando: {self.comandos_field.text}")
            # self.ejecutar_comando(self)

        elif keycode[1] in ('tab','spacebar') and self.comandos_field.focus == False:
            self.comandos_field.focus = True
        print(f"Key press: {keycode[1]}")
    
    # @mainthread
    def btnfunc(self, obj):
        print('Button is pressed!!')
        # self.theme_cls.primary_palette = 'Red'

        # hilollamado = threading.Thread(target=llamado_tkinter, daemon=True)
        # hilollamado.start()
        print(self.screen.size)
        # time.sleep(5)
        # self.agregar_registro(obj)
    
    @mainthread
    def eliminar_registro(self):
        lista_eliminar = []
        lista_registro = self.lista_registro.children
        # lista_registro.reverse()
        if len(lista_registro) >= 60:
            for registro in lista_registro:
                index = lista_registro.index(registro)
                # print(f"Objeto: {registro.text}, Index: {index}")
                if index >= len(lista_registro) / 2:
                    lista_eliminar.append(registro)
                    print(f"Eliminando objeto: {registro.text}, Index: {index}")
                    # self.lista_registro.remove_widget(registro)

            for elemento in lista_eliminar:
                self.lista_registro.remove_widget(elemento)
            
            del lista_eliminar, lista_registro
            # Print the number of objects in memory before collecting
            print("Objects in memory before:", len(gc.get_objects()))

            # Collect any unreferenced objects
            gc.collect()

            # Print the number of objects in memory after collecting
            print("Objects in memory after:", len(gc.get_objects()))

    @mainthread
    def agregar_registro(self, contenido='', color=''):
        # global num, ultimo_reg
        # while not ultimo_reg:
        #     pass
        
        # print(obj)
        # if not contenido:
        #     return
        self.lista_registro.add_widget(
            # OneLineListItem(
            #     text= contenido,
            #     size_hint = (None,None),
            #     size = (self.contenedor_registro.width, "20px"),
                
            # )
    
            MDLabel(
                text= contenido,
                size_hint = (None,None),
                size = (self.contenedor_registro.width, "20px"),
                padding = (10,10),
                adaptive_size = True,
                adaptive_width = True

            )
        )
        if contenido.find('|') == -1:
            self.lista_registro.children[0].halign = "center"
        
        if color:
            self.lista_registro.children[0].color = color
        try:
            lista_registro = self.lista_registro.children   
            if len(lista_registro) >= 60:
                self.eliminar_registro()
        except:
            print(self.lista_registro.children)
        # MDLabel.theme_text_color 
        # OneLineListItem.ad
        """CICLO PARA RECORRER LOS REGISTROS Y MODIFICAR SUS DIMENSIONES"""
        # for elemento in self.lista_registro.children:
        #     print(elemento)
        # MDScrollView.scroll_timeout
        # self.contenedor_registro.scroll_to(self.lista_registro[0])
        lista = self.lista_registro.children
        for child in lista:
            # print(f"CHILD: {child}")
            if lista.index(child) == 0:
                self.contenedor_registro.scroll_to(child)
        # print(self.contenedor_registro.children)
    
    @mainthread
    def cuadro_comandos(self,obj,visible=False):
        global cuadro_comandos_visible
        if visible:
            self.comandos_field.opacity = 1
            self.btn_ejecutar.opacity = 1
            self.comandos_field.select_all()
            self.comandos_field.delete_selection()
            self.comandos_field.focus = True
            # self.comandos_field.paste()
            # self.link = self.link_field.text
            # print(f"link: {self.link}")
            cuadro_comandos_visible = True
            
        else:
            self.comandos_field.opacity = 0
            self.btn_ejecutar.opacity = 0
            cuadro_comandos_visible = False
    
    # @mainthread
    # def cuadro_comandos_visible()
    
    @mainthread
    def ejecutar_comando(self,obj):
        global run
        if self.comandos_field.text != '':
            comando = self.comandos_field.text
            run(modo="texto", comando=comando)
            self.comandos_field.select_all()
            self.comandos_field.delete_selection()
    
    @mainthread
    def salir(self):
        self.stop()
