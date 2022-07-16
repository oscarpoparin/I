import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import os
from tkinter import *
from PIL import Image, ImageTk
import threading as tr
import whatsapp as whapp
import browser
import database
from chatterbot import ChatBot
from chatterbot import preprocessors
from chatterbot.trainers import ListTrainer

#Creacion de ventana principal
                                                                                                                                    
main_window = Tk()                  #ventana raiz
main_window.title("IA Oparin")
main_window.geometry("800x450")     #ancho - alto
main_window.resizable(0, 0)
main_window.configure(bg="#444343")
#main_window.mainloop()             #se ejecutara todo lo que este antes de esta instruccion

#Comandos que podemos usar, Muestra el contenido en interfaz grafica

comandos = """
    Comandos que puedes usar:
    - Reproduce..(canción/video)
    - Busca...(algo)
    - Buscame...(algo)
    - Abre...(página web/app)
    - Archivo...(nombre)
    - Mensaje...(whatsapp)
    - cierra... (app)
    - Cierrate...(fin programa)
"""
#titulo

label_title = Label(
    main_window, 
    text="Oparin AI", 
    bg="#444343", 
    fg="#fff",
    font=('Arial', 30, 'bold')
)
label_title.pack(pady=10)

#contenedor de comandos

canvas_comandos = Canvas(bg="#444343", height=170, width=195)
canvas_comandos.place(x=0, y=0)
canvas_comandos.create_text(90, 80, text=comandos, fill="#fff", font='Arial 10')

#Caja de texto

text_info = Text(main_window, bg="#444343", fg="#fff", font=('Arial', 10))
text_info.place(x=0, y=170, height=280, width=198)

#Agregar imagen 

img = Image.open("machine-learning.png")
img = img.resize((400,240), Image.ANTIALIAS)
img_oparin = ImageTk.PhotoImage(img)
window_photo = Label(main_window, image=img_oparin, bg="#444343")
window_photo.place(x=209, y=70)

#programacion botones

def mexican_voice():
    change_voice(0)

def english_voice():
    change_voice(1)

#funcion para cargar la voz

def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Hola, soy Oparin, tu asistente personal!")

#programacion del programa

name = "Oparin"
listener = sr.Recognizer()
engine = pyttsx3.init()

#codigo para iniciar con una voz por defecto

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)

# diccionario

def charge_data(name_dict, name_file):          #funcion para cargar los datos
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(",")    #tomara como datos a todos los valores que esten antes y despues de una coma
                val = val.rstrip("\n")          #elimina el salto de linea|
                name_dict[key] = val
    except FileNotFoundError as e:
        pass


sites = dict()
charge_data(sites, "pages.txt")
files = dict()
charge_data(files, "archivos.txt")
programs = dict()
charge_data(programs, "apps.txt")
contacts = dict()
charge_data(contacts, "contacts.txt")

#funcion para reproducir audio

def talk(text):
    engine.say(text)
    engine.runAndWait()

#funcion de leer texto en caja de texto y hablar

def read_and_talk():
    text = text_info.get("1.0", "end")  #obtener todo el contenido de principio a fin
    talk(text)

#funcion que escribe lo que encontro en internet y lo escribe en la caja de texto

def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)

#funcion para escuchar audio

def listen(phrase=None):
    listener = sr.Recognizer()    
    with sr.Microphone() as source:            
        listener.adjust_for_ambient_noise(source)
        talk(phrase)
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return rec

#funciones asociadas a las palabras clave del diccionario key_words


def reproduce(rec):                         #funcion para reproducir canciones y videos en youtube
    music = rec.replace('reproduce', '')
    print("Reproduciendo " + music)
    talk("Reproduciendo " + music)
    pywhatkit.playonyt(music)               #abri youtube y busca lo que indiquemos


def busca(rec):                             #funcion para buscar informacion en internet
    search = rec.replace('busca', '')
    wikipedia.set_lang("es")
    wiki = wikipedia.summary(search, 1)
    talk(wiki)
    write_text(search + ": " + wiki)        #guarda lo encontrado en la funcion write_text


def abre(rec):                              #funcion para abrir sitios web y programas
    task = rec.replace('abre', '').strip()

    if task in sites:
        for task in sites:
            if task in rec:
                sub.call(f'start chrome.exe {sites[task]}', shell=True)
                talk(f'Abriendo {task}')
    elif task in programs:
        for task in programs:
            if task in rec:
                talk(f'Abriendo {task}')
                os.startfile(programs[task])
    else:
        talk("Lo siento, parece que aún no has agregado esa app o página web, \
            usa los botones de agregar!")


def archivo(rec):                           #funcion para abrir archivos
    file = rec.replace('archivo', '').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
        talk("Lo siento, parece que aún no has agregado ese archivo, \
            usa los botones de agregar!")


def escribe(rec):                           #funcion para escribir en un archivo de texto
    try:
        with open("nota.txt", 'a') as f:
            write(f)

    except FileNotFoundError as e:
        file = open("nota.txt", 'a')
        write(file)


def enviar_mensaje(rec):                    #funcion para enviar mensaje por whatsapp web
    talk("¿A quién quieres enviar el mensaje?")
    contact = listen("Te escucho")
    contact = contact.strip()

    if contact in contacts:
        for cont in contacts:
            if cont == contact:
                contact = contacts[cont]
                talk("¿Qué mensaje quieres enviarle?")
                message = listen("Te escucho")
                talk("Enviando mensaje...")
                whapp.send_message(contact, message)
    else:
        talk("Parece qué aún no has agregado a ese contacto, usa el botón de agregar!")


def cierra(rec):                                #funcion para cerrar programas qu tengamos agregados
    for task in programs:
        kill_task = programs[task].split('\\')  #guardar los datos en una lista
        kill_task = kill_task[-1]               #obtienen el ultimo elemento de la lista
        if task in rec:
            sub.call(f'TASKKILL /IM {kill_task} /F', shell=True)#comando para cerrar el programa 
            talk(f'Cerrando {task}')
        if 'todo' in rec:
            sub.call(f'TASKKILL /IM {kill_task} /F', shell=True)
            talk(f'Cerrando {task}')
    if 'ciérrate' in rec:
        talk('Adiós!')
        sub.call('TASKKILL /IM python.exe /F', shell=True)#TASKKILL /IM nombre del archivo ejecutable /F


def buscame(rec):                               #funcion para buscar en el buscador de google usando el archivo browser.py
    something = rec.replace('búscame', '').strip()
    talk("Buscando " + something)
    browser.search(something)            

#diccionario para realizacion de los comandos en la funcion principal

key_words = {
    'reproduce': reproduce,
    'busca': busca,
    'abre': abre,
    'archivo': archivo,
    'escribe': escribe,
    'mensaje': enviar_mensaje,
    'cierra': cierra,
    'ciérrate': cierra,
    'búscame': buscame
}

#funcion principal

def run_oparin():
    chat = ChatBot("oparin", database_uri=None)#database_uri=None nos permite borrar del aprendizaje algun dato de nuestra BD
    trainer = ListTrainer(chat)#entrenamiento del bot
    trainer.train(database.get_questions_answers())
    talk("Te escucho...")
    while True:
        try:
            rec = listen("")
        except UnboundLocalError:
            talk("No te entendí, intenta de nuevo")
            continue
        if 'busca' in rec:
            key_words['busca'](rec)#busqueda y acceso a una sola clave del diccionario key_words
            break
        elif rec.split()[0] in key_words:
            key = rec.split()[0]        
            key_words[key](rec)#busqueda y acceso en nuestro directorio key_word
        else:
            print("Tú: ", rec)
            answer = chat.get_response(rec)# obtiene la respuesta del bot
            print("Oparin: ", answer)
            talk(answer)
            if 'chao' in rec:
                break
    main_window.update()#actualizar la ventana y evitamos el error de no responde

#funcion para escribir dentro de un documento de texto

def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen("Te escucho")
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)

#funcion para abrir una nueva ventana y agregar archivos

def open_w_files():
    global namefile_entry, pathf_entry # variables globales
    window_files = Toplevel()#crear nueva ventana
    window_files.title("Agregar archivos")
    window_files.configure(bg="#434343")
    window_files.geometry("300x200")
    window_files.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window_files)} center') # coloca la nueva ventana en el centro

    title_label = Label(
        window_files, 
        text="Agrega un archivo",
        fg="white", 
        bg="#434343", 
        font=('Arial', 15, 'bold')
    )
    title_label.pack(pady=3)
    name_label = Label(
        window_files, 
        text="Nombre del archivo",
        fg="white", 
        bg="#434343", 
        font=('Arial', 10, 'bold')
    )
    name_label.pack(pady=2)

    namefile_entry = Entry(window_files)
    namefile_entry.pack(pady=1)

    path_label = Label(
        window_files, 
        text="Ruta del archivo",
        fg="white", 
        bg="#434343", 
        font=('Arial', 10, 'bold')
    )
    path_label.pack(pady=2)

    pathf_entry = Entry(window_files, width=35)
    pathf_entry.pack(pady=1)

    save_button = Button(
        window_files, 
        text="Guardar", 
        bg='#16222A',
        fg="white", 
        width=8, 
        height=1, 
        command=add_files   #eventos / funciones
    )
    save_button.pack(pady=4)

#funcion para abrir una nueva ventana para agregar programas

def open_w_apps():
    global nameapps_entry, patha_entry
    window_apps = Toplevel()
    window_apps.title("Agregar apps")
    window_apps.configure(bg="#434343")
    window_apps.geometry("300x200")
    window_apps.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window_apps)} center')

    title_label = Label(
        window_apps, 
        text="Agrega una app",
        fg="white", 
        bg="#434343", 
        font=('Arial', 15, 'bold')
    )
    title_label.pack(pady=3)
    name_label = Label(
        window_apps, 
        text="Nombre de la app",
        fg="white", 
        bg="#434343", 
        font=('Arial', 10, 'bold')
    )
    name_label.pack(pady=2)

    nameapps_entry = Entry(window_apps)
    nameapps_entry.pack(pady=1)

    path_label = Label(
        window_apps, 
        text="Ruta de la app",
        fg="white", 
        bg="#434343", 
        font=('Arial', 10, 'bold')
    )
    path_label.pack(pady=2)

    patha_entry = Entry(window_apps, width=35)
    patha_entry.pack(pady=1)

    save_button = Button(
        window_apps, 
        text="Guardar", 
        bg='#16222A',
        fg="white", 
        width=8, 
        height=1, 
        command=add_apps
    )
    save_button.pack(pady=4)

#funcion para abrir una nueva ventana para agregar paginas

def open_w_pages():
    global namepages_entry, pathp_entry
    window_pages = Toplevel()
    window_pages.title("Agregar páginas web")
    window_pages.configure(bg="#434343")
    window_pages.geometry("300x200")
    window_pages.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window_pages)} center')

    title_label = Label(
        window_pages, 
        text="Agrega una página web",
        fg="white", 
        bg="#434343", 
        font=('Arial', 15, 'bold')
    )
    title_label.pack(pady=3)
    name_label = Label(
        window_pages, 
        text="Nombre de la página",
        fg="white", 
        bg="#434343", 
        font=('Arial', 10, 'bold')
    )
    name_label.pack(pady=2)

    namepages_entry = Entry(window_pages)
    namepages_entry.pack(pady=1)

    path_label = Label(
        window_pages, 
        text="URL de la página",
        fg="white", 
        bg="#434343", 
        font=('Arial', 10, 'bold')
    )
    path_label.pack(pady=2)

    pathp_entry = Entry(window_pages, width=35)
    pathp_entry.pack(pady=1)

    save_button = Button(
        window_pages, 
        text="Guardar", 
        bg='#16222A',
        fg="white", 
        width=8, 
        height=1, 
        command=add_pages
    )
    save_button.pack(pady=4)

#funcion para abrir una nueva ventana 

def open_w_contacts():
    global namecontact_entry, phone_entry
    window_contacts = Toplevel()
    window_contacts.title("Agregar un contacto")
    window_contacts.configure(bg="#434343")
    window_contacts.geometry("300x200")
    window_contacts.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window_contacts)} center')

    title_label = Label(
        window_contacts, 
        text="Agrega un contacto",
        fg="white", 
        bg="#434343", 
        font=('Arial', 15, 'bold')
    )
    title_label.pack(pady=3)
    name_label = Label(
        window_contacts, 
        text="Nombre del contacto",
        fg="white", 
        bg="#434343", 
        font=('Arial', 10, 'bold')
    )
    name_label.pack(pady=2)

    namecontact_entry = Entry(window_contacts)
    namecontact_entry.pack(pady=1)

    phone_label = Label(
        window_contacts, 
        text="Número celular (con código del país).",
        fg="white", 
        bg="#434343", 
        font=('Arial', 10, 'bold')
    )
    phone_label.pack(pady=2)

    phone_entry = Entry(window_contacts, width=35)
    phone_entry.pack(pady=1)

    save_button = Button(
        window_contacts, 
        text="Guardar", 
        bg='#16222A',
        fg="white", 
        width=8, 
        height=1, 
        command=add_contacts
    )
    save_button.pack(pady=4)

#funcion boton segunda ventana para guardar archivos

def add_files():
    name_file = namefile_entry.get().strip()# recibe el valor de la variable y comprueba si esta vacio
    path_file = pathf_entry.get().strip()

    files[name_file] = path_file
    save_data(name_file, path_file, "archivos.txt")
    namefile_entry.delete(0, "end")#borra los datos despues de que los guarda
    pathf_entry.delete(0, "end")

#funcion boton segunda ventana para guardar apps

def add_apps():
    name_file = nameapps_entry.get().strip()
    path_file = patha_entry.get().strip()

    programs[name_file] = path_file
    save_data(name_file, path_file, "apps.txt")
    nameapps_entry.delete(0, "end")
    patha_entry.delete(0, "end")

#funcion boton segunda ventana para guardar archivos

def add_pages():
    name_page = namepages_entry.get().strip()
    url_pages = pathp_entry.get().strip()

    sites[name_page] = url_pages
    save_data(name_page, url_pages, "pages.txt")
    namepages_entry.delete(0, "end")
    pathp_entry.delete(0, "end")

#funcion boton segunda ventana para guardar datos de los contactos

def add_contacts():
    name_contact = namecontact_entry.get().strip()
    phone = phone_entry.get().strip()

    contacts[name_contact] = phone
    save_data(name_contact, phone, "contacts.txt")
    namecontact_entry.delete(0, "end")
    phone_entry.delete(0, "end")

#funcion para guardar los datos agregados 'archivos,paginas,programas'

def save_data(key, value, file_name):
    try:
        with open(file_name, 'a') as f:
            f.write(key + "," + value + "\n")
    except FileNotFoundError:
        file = open(file_name, 'a')
        file.write(key + "," + value + "\n")

#funciones para mostrar los los datos agregados

def talk_pages():
    if bool(sites) == True:
        talk("Has agregado las siguientes páginas web")
        for site in sites:
            talk(site)
    else:
        talk("Aún no has agregado páginas web!")


def talk_apps():
    if bool(programs) == True:
        talk("Has agregado las siguientes apps")
        for app in programs:
            talk(app)
    else:
        talk("Aún no has agregado apps!")


def talk_files():
    if bool(files) == True:
        talk("Has agregado los siguientes archivos")
        for file in files:
            talk(file)
    else:
        talk("Aún no has agregado archivos!")

def talk_contacts():
    if bool(contacts) == True:
        talk("Has agregado los siguientes contactos")
        for cont in contacts:
            talk(cont)
    else:
        talk("Aún no has agregado contactos!")

#funcion para preguntas nombre

def give_me_name():
    talk("Hola, ¿cómo te llamas?")
    name = listen("Te escucho")
    name = name.strip()
    talk(f"Bienvenido {name}")

    try:
        with open("name.txt", 'w') as f:
            f.write(name)
    except FileNotFoundError:
        file = open("name.txt", 'w')
        file.write(name)

#funcion para ejecutar la funcion al iniciar el programa

def say_hello():

    if os.path.exists("name.txt"):
        with open("name.txt") as f:
            for name in f:
                talk(f"Hola, bienvenido {name}")
    else:
        give_me_name()

#hilo

def thread_hello():
    t = tr.Thread(target=say_hello)
    t.start()#inicializa el hilo


thread_hello()

#creacion de botones

button_voice_mx = Button(
                            main_window, 
                            text="Idioma Español", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 12, "bold"),
                            border=0,
                            command= mexican_voice #funcion del boton / eventos
                         )

button_voice_us = Button(
                            main_window, 
                            text="Idioma English", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 12, "bold"),
                            border=0,
                            command= english_voice #funcion del boton / eventos
                         )

button_listen = Button(
                            main_window, 
                            text="Escuchar", 
                            bg="#1565c0",
                            fg="#fff",
                            font=("Arial", 15, "bold"),
                            width=20,
                            height=1,
                            command= run_oparin #funcion del boton / eventos
                         )

button_speak = Button(
                            main_window, 
                            text="Hablar", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 12, "bold"),
                            border=0,
                            command= read_and_talk #funcion del boton / eventos
                         )

button_add_files = Button(
                            main_window, 
                            text="Agregar Archivos", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 12, "bold"),
                            border=0,
                            command= open_w_files #funcion del boton / eventos
                         )

button_add_apps = Button(
                            main_window, 
                            text="Agregar Apps", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 12, "bold"),
                            border=0,
                            command= open_w_apps #funcion del boton / eventos
                         )

button_add_pages = Button(
                            main_window, 
                            text="Agregar Paginas", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 12, "bold"),
                            border=0,
                            command= open_w_pages #funcion del boton / eventos
                         ) 

button_tell_pages = Button(
                            main_window, 
                            text="Paginas Agregadas", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 9, "bold"),
                            border=0,
                            command= talk_pages #funcion del boton / eventos
                         ) 

button_tell_apps = Button(
                            main_window, 
                            text="Programas Agregados", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 9, "bold"),
                            border=0,
                            command= talk_apps #funcion del boton / eventos
                         ) 
                        
button_tell_files = Button( 
                            main_window, 
                            text="Archivos Agregados", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 9, "bold"),
                            border=0,
                            command= talk_files #funcion del boton / eventos
                        ) 

button_add_contacts = Button( 
                            main_window, 
                            text="Agregar Contacto", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 12, "bold"),
                            border=0,
                            command= open_w_contacts #funcion del boton / eventos
                         ) 

button_tell_contacts = Button( 
                            main_window, 
                            text="Contactos Agregados", 
                            bg="#444343",
                            fg="#fff",
                            font=("Arial", 9, "bold"),
                            border=0,
                            command= talk_contacts #funcion del boton / eventos
                         ) 
#posicionamiento de botones

#vertical
button_voice_mx.place(x=635, y=80, width=150, height=30) # horizontal, vertical, ancho, alto
button_voice_us.place(x=635, y=140, width=150, height=30)
button_speak.place(x=635, y=200, width=150, height=30) # boton escuchar
button_listen.pack(side= BOTTOM, pady=10)
button_add_files.place(x=635, y=260, width=150, height=30)
button_add_apps.place(x=635, y=320, width=150, height=30)
button_add_pages.place(x=635, y=380, width=150, height=30)
button_add_contacts.place(x=635, y=380, width=150, height=30)

#botones acomodados de forma horizontal

button_tell_pages.place(x=205, y=320, width=128, height=30)
button_tell_apps.place(x=338, y=320, width=140, height=30)
button_tell_files.place(x=483, y=320, width=128, height=30)
button_tell_contacts.pack(side=BOTTOM, pady=3)


main_window.mainloop()