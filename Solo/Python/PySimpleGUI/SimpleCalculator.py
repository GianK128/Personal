# KEBERLEIN, Gian Franco - (WIP)

import PySimpleGUI as sg

bg_color = "#23283d"                # TODO: Buscar un color mas bonito

btn_type_number: dict = {}
btn_type_operation: dict = {}
btn_type_equals: dict = {}
txt_type_display: dict = { "font" : ("Helvetica", 20), "text_color" : "red", "background_color" : "black", "justification" : "rigth"}
txt_type_bg: dict = { "font" : ("Helvetica", 10), "text_color" : "white", "background_color" : bg_color, "justification" : "rigth"}

layout: list = [
    [sg.Text("Python Calculator", size = (40, 1), **txt_type_bg)],
    [sg.Text("", size = (40, 1), **txt_type_display)]
]

window: object = sg.Window("Python Calculator", layout = layout, background_color = bg_color, size = (320, 270))

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break