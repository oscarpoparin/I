import webbrowser
import pyautogui as at
import time

#funcion para enviar mensajes por whatsapp web

def send_message(contact, message):
    webbrowser.open(f"https://web.whatsapp.com/send?phone={contact}&text={message}")    # abre whatsapp web, busca el numero y tomara el mensaje y colocara en la caja del chat
    time.sleep(20)                                                                       # pausa por un periodo de tiempo
    at.press('enter')                                                                   # se enviara el mensaje al precionar enter