import pyautogui as gui
import time
import webbrowser as wb
import datetime as dt
import PySimpleGUI as sg

sg.theme('Dark Green 7') # Dark Green 5/7

txt_type_h1 = {'size':(10,2), 'justification':'center', 'font':('Helvetica', 20)}
txt_type_h2 = {'size':(30,1), 'font':('Helvetica', 15, 'underline')}

weekday_values = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
time_values = []

def populate_time_values():
    cicles = 6 * 24 - 1 
    h = dt.datetime.now().replace(hour=0, minute=0)
    d = dt.timedelta(minutes=10)
    time_values.append(dt.datetime.strftime(h, '%H:%M'))

    for c in range(cicles):
        h += d
        time_values.append(dt.datetime.strftime(h, '%H:%M'))

populate_time_values()

layout = [
    [sg.Text("Classroom\nPresente-Bot", **txt_type_h1), sg.Image(filename="images/classroom-logo.png", pad=((15,0),(0,0)))],
    [sg.HorizontalSeparator()],
    [sg.Text("Datos de Classroom", **txt_type_h2)],
    [sg.Text("Enlace de la clase:", size=(23,1)), sg.Input(size=(43,1))],
    [sg.Text("Imagen de header de la clase:", size=(23,1)), sg.Input(size=(35,1)), sg.FileBrowse(button_text="Buscar", size=(5, 1))],
    [sg.Text("Imagen de caja de comentario:", size=(23,1)), sg.Input(size=(35,1)), sg.FileBrowse(button_text="Buscar", size=(5, 1))],
    [sg.HorizontalSeparator()],
    [sg.Text("Datos de tiempo", **txt_type_h2)],
    [sg.Text("Día de la semana:"), sg.Combo(values=weekday_values, default_value='Lunes', size=(15,1)), sg.Text("Hora del día:"), sg.Spin(values=time_values, size=(10,1))],
    [sg.Text("- Tiempo de espera del navegador:", size=(30,1)),sg.Text("- Tiempo de espera entre chequeos:")],
    [sg.Input(size=(10,1), justification='right'), sg.Text("segundos.", size=(20,1)), sg.Input(size=(10,1), justification='right'), sg.Text("minutos.")],
    [sg.HorizontalSeparator()],
    [sg.Text("Mensaje", **txt_type_h2)],
    [sg.Input(size=(72,1))],
    [sg.Submit('Guardar configuración', size=(20, 2), pad=((9,0),(10,10))), sg.VerticalSeparator(pad=((9,0),(10,10))), sg.Submit('Correr programa', size=(38, 2), pad=((11,0),(10,10)))]
]

window = sg.Window(title="Classroom Presente-Bot", layout=layout)

while True:
    event, value = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()

# LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO, DOMINGO = range(7)

# #================================MACROS================================#
# # ESTA SECCION TIENE LA INFO QUE COMO USUARIO HAY QUE CAMBIAR.
# # SI USA ESTA APP COMO USUARIO NO CAMBIE NADA MAS ALLA DE ESTOS VALORES.
# # PARA MAS INFORMACION SOBRE CADA VALOR, LEA EL README ADJUNTO
# MESSAGE = "Hello, World!"                                           # Mensaje a escribir
# IMG2FIND = "images/to-find.png"                                     # Ruta de la imagen del campo donde se va a escribir
# CLASS_HEADER_IMG = "images/header.png"                              # Ruta de la imagen del Header de la clase
# CLASS_URL = "https://classroom.google.com/u/0/c/xxxxxxxxxxxxxxxx"   # URL de la clase a la que entrar
# WAITBROWSER_SECONDS = 20                                            # Tiempo de espera despues de abrir el navegador para actuar (en segundos)
# WAITDATETIME_MINUTES = 0.1                                          # Tiempo de espera entre cada chequeo por la hora (en minutos)
# WEEKDAY = LUNES                                                     # Dia de la semana esperado para enviar el mensaje
# TIME = "00:00"                                                      # Hora esperada para enviar el mensaje
# #======================================================================#

# s_hour, s_min = TIME.split(":")

# while True:
#     weekday = dt.date.today().weekday()

#     if weekday == WEEKDAY:
#         print("Checked day. Checking time...")

#         now = dt.datetime.now()
#         if now.hour >= int(s_hour) and now.minute >= int(s_min):
#             print("Checked time. Opening browser...")
#             break
#         print(f"Not the time. Checking again in {WAITDATETIME_MINUTES} minutes.")
#         time.sleep(WAITDATETIME_MINUTES * 60)
#     else:
#         print(f"Today is not the day. Checking again in {WAITDATETIME_MINUTES} minutes.")
#         time.sleep(WAITDATETIME_MINUTES * 60)

#     time.sleep(1)

# width, height = gui.size()

# wb.open(CLASS_URL)
# time.sleep(WAITBROWSER_SECONDS)

# while True:
#     if gui.locateOnScreen(CLASS_HEADER_IMG) is not None:
#         print("Found class header image.")
#         gui.moveTo(width / 2, height / 2)
#         break
#     print("Can not find class header image. Trying again in 3 seconds.")
#     time.sleep(3)

# while True:
#     try:
#         comment = gui.locateOnScreen(IMG2FIND)
#         center_x = comment.left + (comment.width / 2)
#         center_y = comment.top + (comment.height / 2)
#         send_x = comment.left + (comment.width * 0.95)

#         print("Found comment image.")

#         gui.click(center_x, center_y)
#         gui.write(MESSAGE)
#         gui.click(send_x, center_y)

#         print("Comment sent! Finishing...")
#         break
#     except AttributeError:
#         print("Could not find comment image, scrolling down, trying again.")
#         gui.scroll(-100)
#         time.sleep(1)
