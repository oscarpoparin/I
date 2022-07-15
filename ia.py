import speech_recognition as sr
import subprocess as sub
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, os
from pygame import mixer
import threading as tr


name = "oparin"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')  # coloca una voz
# colocar voz que este en esa posicion
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 145)

#diccionario

sites = {
            'google':'google.com',
            'youtube':'youtube.com',
            'facebook':'facebook.com',
            'whatsapp':'web.whatsapp.com'
        }

files = {
            'nuevo':'nuevo - nuevo.txt'
        }

programs = {
                'photoshop':r"D:\Photoshop\Adobe Photoshop 2022\Photoshop.exe",
                'word':r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
            }

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("puedes decir algo...")
            talk("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')

    except:
        pass
    return rec

def run_oparin():
    while True:
        rec = listen()
        if 'reproduce' in rec:
            music = rec.replace('reproduce','')
            print("reproduciendo" + music)
            talk("Reproduciendo" + music)
            pywhatkit.playonyt(music)#abri youtube y busca lo que indiquemos
        elif 'busca' in rec:
            search = rec.replace('busca','')
            print('Buscando' + search)
            talk('Buscando' + search)
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search + ": " + wiki)
            talk(wiki)
        elif 'abre' in rec:
            for site in rec:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell = True)
                    talk(f'Abriendo {site}')
            for app in programs:
                if app in rec:
                    talk(f'Abriendo {app}')
                    os.startfile(programs[app])
        #elif 'archivo' in rec: 
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell = True)
                    talk(f'Abriendo {file}')
        elif 'escribe' in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write(f)

            except FileNotFoundError as e:
                file = open("nota.txt", 'w')
                write(file)
        elif 'termina' in rec:
            talk("adios")
            break

def write(f):
    talk("¿Que deseas que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, ya puedes reviar el documento...")
    sub.Popen("nota.txt", shell = True)

if __name__ == '__main__':
    run_oparin()