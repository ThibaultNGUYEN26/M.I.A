# M.I.A : Mon Intelligence Artificielle

# [---------- IMPORTS ----------]

import pyttsx3
import speech_recognition as sr
import subprocess
import datetime
import random
import wikipedia
import webbrowser as wb
import os
import requests
import json
from decimal import Decimal, getcontext
import csv
import wmi
import ctypes
from covid import Covid
import pyautogui
import string
from win32com.client import GetObject
import cv2
import numpy as np
import face_recognition
import time
from pydub import AudioSegment
from pydub.playback import play
import dlib
import PIL.Image
from imutils import face_utils
import argparse
from pathlib import Path
import ntpath
from google_trans_new import google_translator
import serial
import webbrowser
import winshell
import wolframalpha
import operator


# [---------- INITIALISATIONS ----------]

engine = pyttsx3.init()

# key_word = {"mia":["mia","Mia","milla","Milla"]}
translator = google_translator() 


def do_nothing():
    print("M.I.A : ")


# Fonction qui considère la demande
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[INFO] Ecoute...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("[INFO] Acquisition de votre demande...")
        command = r.recognize_google(audio, language="fr-fr")
        print("[INFO] Utilisateur : " + command)
        print("...")
    except Exception as e:
        print(e)
        print("M.I.A : Je n'ai pas compris, pouvez-vous répéter ?")
        # mia("Je n'ai pas compris, pouvez-vous répéter ?")
        return "None"
    
    return command


# Fonction qui fait parler M.I.A
def mia(audio):
    led_on()
    engine.say(audio)
    engine.runAndWait()










# [---------- FONCTIONS ----------]

arduinoData = serial.Serial('COM5', 9600)


def led_on():
    arduinoData.write("1".encode())


def led_off():
    arduinoData.write("0".encode())


# Fonction qui appelle temperature()
def activate_temperature():
    arduinoData.write("2".encode())
    temperature()


# Fonction qui donne la température
def temperature():
    for i in range(2):
        data = arduinoData.readline()
        print("M.I.A : " + str(data, 'utf-8') + ".")
        mia(str(data, 'utf-8'))
        led_off()


# Fonction Arduino Test
def arduino_control():

    print("M.I.A : Vous êtes dans l'Arduino.")
    mia("Vous êtes dans l'Arduino.")
    led_off()

    ser = serial.Serial('COM5', 9600)
    time.sleep(1)

    user_input = 'e'

    test = True

    while test:
        user_input = take_command()
        if 'rouge' in user_input:
            ser.write('r'.encode("ascii"))
            print("M.I.A : J'allume la led rouge.")
            mia("J'allume la led rouge.")
            led_off()
        elif 'bleu' in user_input:
            ser.write('b'.encode("ascii"))
            print("M.I.A : J'allume la led bleu.")
            mia("J'allume la led bleu.")
            led_off()
        elif 'vert' in user_input or 'verte' in user_input:
            ser.write('g'.encode("ascii"))
            print("M.I.A : J'allume la led verte.")
            mia("J'allume la led verte.")
            led_off()
        elif 'jaune' in user_input:
            ser.write('y'.encode("ascii"))
            print("M.I.A : J'allume la led jaune.")
            mia("J'allume la led jaune.")
            led_off()
        elif 'quitter' in user_input or 'quitte' in user_input:
            test = False
        elif 'éteins' in user_input or 'éteindre' in user_input:
            print("M.I.A : J'éteins les led.")
            mia("J'éteins les led.")
            led_off()
            ser.write('e'.encode("ascii"))
        time.sleep(0.5)

    print("M.I.A : Vous avez quitter Arduino.")
    mia("Vous avez quitter Arduino.")
    led_off()
    ser.close()


# Fonction de reconnaissance faciale
def reco_fac():
    # print('[INFO] Starting System...')
    # print('[INFO] Importing pretrained model...')
    pose_predictor_68_point = dlib.shape_predictor('pretrained_model/shape_predictor_68_face_landmarks.dat')
    pose_predictor_5_point = dlib.shape_predictor('pretrained_model/shape_predictor_5_face_landmarks.dat')
    face_encoder = dlib.face_recognition_model_v1("pretrained_model/dlib_face_recognition_resnet_model_v1.dat")
    face_detector = dlib.get_frontal_face_detector()


    def transform(image, face_locations):
        coord_faces = []
        for face in face_locations:
            rect = face.top(), face.right(), face.bottom(), face.left()
            coord_face = max(rect[0], 0), min(rect[1], image.shape[1]), min(rect[2], image.shape[0]), max(rect[3], 0)
            coord_faces.append(coord_face)
        return coord_faces


    def encode_face(image):
        face_locations = face_detector(image, 1)
        face_encoding_list = []
        landmarks_list = []
        for face_location in face_locations:
            shape = pose_predictor_68_point(image, face_location)
            face_encoding_list.append(np.array(face_encoder.compute_face_descriptor(image, shape, num_jitters=1)))
            shape = face_utils.shape_to_np(shape)
            landmarks_list.append(shape)
        face_locations = transform(image, face_locations)
        return face_encoding_list, face_locations, landmarks_list


    def easy_face_reco(frame, known_face_encodings, known_face_names):
        # global test
        rgb_small_frame = frame[:, :, ::-1]
        # ENCODING FACE
        face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
        face_names = []
        for face_encoding in face_encodings_list:
            if len(face_encoding) == 0:
                return np.empty((0))
            # CHECK DISTANCE BETWEEN KNOWN FACES AND FACES DETECTED
            vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
            tolerance = 0.6
            result = []
            for vector in vectors:
                if vector <= tolerance:
                    result.append(True)
                else:
                    result.append(False)
            if True in result:
                first_match_index = result.index(True)
                name = known_face_names[first_match_index]
            else:
                name = "Inconnu"
            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations_list, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
            cv2.rectangle(frame, (left, bottom + 40), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 30, bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        for shape in landmarks_list:
            for (x, y) in shape:
                cv2.circle(frame, (x, y), 1, (255, 0, 255), -1)


    if __name__ == '__main__':
        test = True

        # print('[INFO] Importing faces...')
        face_to_encode_path = ['recognition_images/thibault.jpg', 'recognition_images/salome.jpg', 'recognition_images/maman.jpg']
        known_face_encodings = []
        for face_to_encode_path in face_to_encode_path:
            image = PIL.Image.open(face_to_encode_path)
            image = np.array(image)
            face_encoded = encode_face(image)[0][0]
            known_face_encodings.append(face_encoded)
        known_face_names = ['Thibault', 'Salome', 'Maman']
        # print('[INFO] Faces well imported')

        print('\n[INFO] Starting Webcam...')
        video_capture = cv2.VideoCapture(0)
        # print('[INFO] Webcam well started')
        print('[INFO] Facial Recognition...')
        while test:
            ret, frame = video_capture.read()
            easy_face_reco(frame, known_face_encodings, known_face_names)

            cv2.imshow('Reconnaissance Faciale', frame)

            rgb_small_frame = frame[:, :, ::-1]
            # ENCODING FACE
            face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
            face_names = []
            for face_encoding in face_encodings_list:
                vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
                tolerance = 0.6
                result = []
                for vector in vectors:
                    if vector <= tolerance:
                        result.append(True)
                    else:
                        result.append(False)
                if True in result:
                    first_match_index = result.index(True)
                    name = known_face_names[first_match_index]
                    
                    if name == 'Thibault':
                        print('[INFO] Reconnaissance de Thibault')
                        print('[INFO] Stopping Webcam...\n')
                        video_capture.release()
                        cv2.destroyAllWindows()

                        test = False

                    elif name == "Salome":
                        print('[INFO] Reconnaissance de Salomé')
                        print('[INFO] Stopping Webcam...\n')
                        video_capture.release()
                        cv2.destroyAllWindows()

                        hour = datetime.datetime.now().hour
                        if(hour >= 6 and hour < 20):
                            print("M.I.A : Bonjour Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                            mia("Bonjour Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                            led_off()
                            print("M.I.A : Cheh")
                            mia("Cheh")
                            led_off()
                        else:
                            print("M.I.A : Bonsoir Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                            mia("Bonsoir Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                            led_off()
                            print("M.I.A : Cheh")
                            mia("Cheh")
                            led_off()

                        WMI = GetObject('winmgmts:')
                        processes = WMI.InstancesOf('Win32_Process')

                        for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
                            print("Killing PID:", p.Properties_('ProcessId').Value)
                            os.system("taskkill /pid "+str(p.Properties_('ProcessId').Value))

                    elif name == "Maman":
                        print('[INFO] Reconnaissance de la maman du Boss')
                        print('[INFO] Stopping Webcam...\n')
                        video_capture.release()
                        cv2.destroyAllWindows()

                        hour = datetime.datetime.now().hour
                        if(hour >= 6 and hour < 20):
                            print("M.I.A : Bonjour la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                            mia("Bonjour la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                            led_off()
                            print("M.I.A : Salut")
                            mia("Salut")
                            led_off()
                        else:
                            print("M.I.A : Bonsoir la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                            mia("Bonsoir la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                            led_off()
                            print("M.I.A : Salut")
                            mia("Salut")
                            led_off()

                        WMI = GetObject('winmgmts:')
                        processes = WMI.InstancesOf('Win32_Process')

                        for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
                            print("Killing PID:", p.Properties_('ProcessId').Value)
                            os.system("taskkill /pid "+str(p.Properties_('ProcessId').Value))

                else:
                    name = "Inconnu"
                face_names.append(name)
            
            key = cv2.waitKey(1)
            if key == 27:
                break
                video_capture.release()
                cv2.destroyAllWindows()
                WMI = GetObject('winmgmts:')
                processes = WMI.InstancesOf('Win32_Process')

                for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
                    print("Killing PID:", p.Properties_('ProcessId').Value)
                    os.system("taskkill /pid "+str(p.Properties_('ProcessId').Value))

    return test


# Truc pour gérer le son
# Import the SendInput object
SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBoardInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time",ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBoardInput),
        ("mi", MouseInput),
        ("hi", HardwareInput)
    ]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

def key_down(keyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBoardInput(keyCode, 0x48, 0, 0, ctypes.pointer(extra))
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def key_up(keyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBoardInput(keyCode, 0x48, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def key(key_code, length = 0):    
    key_down(key_code)
    time.sleep(length)
    key_up(key_code)

def volume_up():
    key(VK_VOLUME_UP)

def volume_down():
    key(VK_VOLUME_DOWN)

def volume_mute():
    key(VK_VOLUME_MUTE)

def set_volume(amount):
    for i in range(0, 50):
        volume_down()
    for i in range(amount // 2):
        volume_up()


# Fonction heure
def time_hour():
    Time = datetime.datetime.now().strftime("%H:%M")
    return Time


# Fonction date
def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    month_letter = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    day = int(datetime.datetime.now().day)
    now = datetime.datetime.today()
    if now.weekday() == 0:
        today = "Lundi"
    elif now.weekday() == 1:
        today = "Mardi"
    elif now.weekday() == 2:
        today = "Mercredi"
    elif now.weekday() == 3:
        today = "Jeudi"
    elif now.weekday() == 4:
        today = "Vendredi"
    elif now.weekday() == 5:
        today = "Samedi"
    elif now.weekday() == 6:
        today = "Dimanche"

    say_date = today + " " + str(day) + "/" + str(month) + "/" + str(year)

    return say_date


# Fonction première discussion
def premier():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    month_letter = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    day = int(datetime.datetime.now().day)
    now = datetime.datetime.today()
    my_age = now.year - 2001

    if now.weekday() == 0:
        today = "Lundi"
    elif now.weekday() == 1:
        today = "Mardi"
    elif now.weekday() == 2:
        today = "Mercredi"
    elif now.weekday() == 3:
        today = "Jeudi"
    elif now.weekday() == 4:
        today = "Vendredi"
    elif now.weekday() == 5:
        today = "Samedi"
    elif now.weekday() == 6:
        today = "Dimanche"
    Time = datetime.datetime.now().strftime("%I:%M")

    hour = datetime.datetime.now().hour
    if(hour >= 6 and hour < 20):
        print("M.I.A : Bonjour boss.")
        mia("Bonjour boss.")
        led_off()
    else:
        print("M.I.A : Bonsoir boss.")
        mia("Bonsoir boss.")
        led_off()

    print("M.I.A : On est le " + date() + " et il est " + time_hour() + ".")
    mia("On est le " + date() + " et il est " + time_hour())
    led_off()

    # Christmas
    if(now.day == 25 and now.month == 12):
        print("Je vous souhaite un joyeux Noël.")
        mia("Je vous souhaite un joyeux Noël.")
        led_off()

    # New year
    if(now.day == 1 and now.month == 1):
        print("Je vous souhaite une bonne année " + str(now.year) + ".")
        mia("Je vous souhaite une bonne année " + str(now.year))
        led_off()

    # Birthday
    if(now.day == 26 and now.month == 5):
        print("Je vous souhaite un joyeux anniversaire pour vos " + str(my_age) + " ans.")
        mia("Je vous souhaite un joyeux anniversaire pour vos " + str(my_age) + " ans.")
        led_off()

    # M.I.A : Birthday
    mia_birthday()


# Fonction qui donne les infos systeme
def info_sys():
    c = wmi.WMI()
    my_system = c.Win32_ComputerSystem()[0]

    print(f"Manufacturer : {my_system.Manufacturer}")
    print(f"Model : {my_system.Model}")
    print(f"Name : {my_system.Name}")
    print(f"Number of Processors : {my_system.NumberOfProcessors}")
    print(f"SystemType : {my_system.SystemType}")
    print(f"SystemFamily : {my_system.SystemFamily}")


# Fonction qui donne le temps restant avant Noël
def christmas():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    now = datetime.datetime.today()

    christmas_month_left = now.year - now.year + 12 - now.month
    christmas_day_left = 25 - now.day

    if christmas_month_left < 0:
        year += 1

    if christmas_month_left == 0:
        print("M.I.A : Noël c'est dans " + str(christmas_day_left) + " jours.")
        mia("Noël c'est dans " + str(christmas_day_left) + " jours.")
        led_off()
    else:
        print("M.I.A : Noël c'est dans " + str(christmas_month_left) + " mois et " + str(christmas_day_left) + " jours.")
        mia("Noël c'est dans " + str(christmas_month_left) + " moi et " + str(christmas_day_left) + " jours.")
        led_off()


# Fonction qui donne le temps restant avant le Nouvel An
def newYear():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    now = datetime.datetime.today()

    newYear_year = now.year + 1
    newYear_month_left = 12 - now.month
    newYear_day_left = now.day - 1

    if newYear_month_left == 0:
        print("M.I.A : Le nouvel an c'est dans " + str(newYear_day_left) + " jours.")
        mia("Le nouvel en c'est dans " + str(newYear_day_left) + " jours.")
        led_off()
    else:
        print("M.I.A : Le nouvel an c'est dans " + str(newYear_month_left) + " mois et " + str(newYear_day_left) + " jours.")
        mia("Le nouvel en c'est dans " + str(newYear_month_left) + " moi et " + str(newYear_day_left) + " jours.")
        led_off()


# Fonction qui donne le temps restant avant mon anniversaire
def birthday():
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    now = datetime.datetime.today()

    birthday_month_left = 5 - now.month
    birthday_day_left = 26 - now.day
    
    if now.day > 26:
        birthday_day_left = now.day - 26
    if now.month > 5:
        birthday_month_left = now.month - 5

    if birthday_month_left == 0:
        print("M.I.A : Votre anniversaire est dans " + str(birthday_day_left) + " jours.")
        mia("Votre anniversaire est dans " + str(birthday_day_left) + " jours.")
        led_off()
    else:
        print("M.I.A : Votre anniversaire est dans " + str(birthday_month_left) + " mois et " + str(birthday_day_left) + " jours.")
        mia("Votre anniversaire est dans " + str(birthday_month_left) + " moi et " + str(birthday_day_left) + " jours.")
        led_off()


# Fonction qui donne l'age de M.I.A
def mia_birthday():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    now = datetime.datetime.today()

    if(now.day == 1 and now.month == 3):
        mia_age = now.year - 2021
        if(mia_age == 1):
            print(f"M.I.A : C'est mon anniversaire, j'ai {mia_age} an.")
            mia(f"C'est mon anniversaire, j'ai {mia_age} an.")
            led_off()
        else:
            print(f"M.I.A : C'est mon anniversaire, j'ai {mia_age} ans.")
            mia(f"C'est mon anniversaire, j'ai {mia_age} ans.")
            led_off()
    else:
        pass


# Fonction qui lance les applications
def application(command):
    if command != None:
        dico_apps = {
            "google":["google","internet","brave"],
            "youtube":["YouTube","youtube","You Tube","you tube"],
            "gmail":["mail", "gmail", "e-mail"],
            "netflix":["netflix"],
            "spotify":["spotify"],
            "vsc":["vs code","visual studio code"],
            "steam":["steam"],
            "minecraft":["minecraft"],
            "discord":["discord"],
            "paint.net":["paint", "paint point net", "paint.net"],
            "terminal":["terminal", "cmd"],
            "calculatrice":["calculatrice","calculette"],
            "ent":["ent", "ent-uca"],
            "ig":["instant gaming"],
            "aternos":["aternos"],
            "amazon":["amazon"],
            "cdiscount":["cdiscount"],
            "twitch":["twitch"],
            "camtasia":["camtasia", "camtasia studio 8"],
            "jeux":["jeux","dossier de jeux", "le dossier de jeux", "mon dossier de jeux"],
            "logiciels":["logiciels", "dossier de logiciels", "mon dossier de logiciels", "le dossier de logiciels" "logiciel", "dossier de logiciel", "mon dossier de logiciel", "le dossier de logiciel"],
            "code":["code", "mon dossier de code", "le dossier de code", "codes", "mon dossier de codes", "le dossier de codes"],
            "bureau":["bureau", "le bureau", "mon bureau"],
            "teams":["teams"]
        }
        fini = False
        while not fini:
            for x in dico_apps["google"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Google.")
                    mia("J'ouvre Google.")
                    led_off()
                    bravepath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
                    wb.get(bravepath).open_new_tab("https://www.google.com")
                    fini = True
            for x in dico_apps["youtube"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre YouTube.")
                    mia("J'ouvre You tube.")
                    led_off()
                    bravepath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
                    wb.get(bravepath).open_new_tab("https://www.youtube.com")
                    fini = True
            for x in dico_apps["gmail"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Gmail.")
                    mia("J'ouvre G-mail.")
                    led_off()
                    bravepath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
                    wb.get(bravepath).open_new_tab("https://www.gmail.com")
                    fini = True
            for x in dico_apps["netflix"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Netflix.")
                    mia("J'ouvre Netflix.")
                    led_off()
                    bravepath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
                    wb.get(bravepath).open_new_tab("https://www.netflix.com/fr/")
                    fini = True
            for x in dico_apps["spotify"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Spotify.")
                    mia("J'ouvre spotify.")
                    led_off()
                    subprocess.Popen('C:/Users/Thibault/AppData/Roaming/Spotify/Spotify.exe')
                    fini = True
            for x in dico_apps["vsc"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Visual Studio Code.")
                    mia("J'ouvre Visual Studio Code.")
                    led_off()
                    subprocess.Popen('C:/Users/Thibault/AppData/Local/Programs/Microsoft VS Code/Code.exe')
                    fini = True
            for x in dico_apps["steam"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Steam.")
                    mia("J'ouvre Steam.")
                    led_off()
                    subprocess.Popen('D:/Program Files (x86)/Steam/Steam.exe')
                    fini = True
            for x in dico_apps["minecraft"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Minecraft.")
                    mia("J'ouvre Minecraft.")
                    led_off()
                    subprocess.Popen('C:/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe')
                    fini = True
            for x in dico_apps["discord"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Discord.")
                    mia("J'ouvre Discord.")
                    led_off()
                    subprocess.Popen('C:/Users/Thibault/AppData/Local/Discord/Update.exe --processStart Discord.exe')
                    fini = True
            for x in dico_apps["paint.net"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Paint.net.")
                    mia("J'ouvre Paint point net.")
                    led_off()
                    subprocess.Popen('C:/Program Files/paint.net/PaintDotNet.exe')
                    fini = True
            for x in dico_apps["terminal"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre l'invite de commande.")
                    mia("J'ouvre l'invite de commande.")
                    led_off()
                    subprocess.Popen('C:/Windows/System32/cmd.exe')
                    fini = True
            for x in dico_apps["calculatrice"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre la calculatrice.")
                    mia("J'ouvre la calculatrice.")
                    led_off()
                    subprocess.Popen('C:/Windows/System32/calc.exe')
                    fini = True
            for x in dico_apps["ent"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre l'ENT.")
                    mia("J'ouvre l'ENT.")
                    led_off()
                    bravepath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
                    wb.get(bravepath).open_new_tab("https://ent.uca.fr/cas/login?service=https%3A%2F%2Fent.uca.fr%2Fcore%2Fhome%2F")
                    fini = True
            for x in dico_apps["ig"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Instant-Gaming.")
                    mia("J'ouvre Instant-Gaming.")
                    led_off()
                    bravepath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
                    wb.get(bravepath).open_new_tab("https://www.instant-gaming.com/fr/")
                    fini = True
            for x in dico_apps["aternos"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Aternos.")
                    mia("J'ouvre Aternosse.")
                    led_off()
                    bravepath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
                    wb.get(bravepath).open_new_tab("https://aternos.org/:fr/")
                    fini = True
            for x in dico_apps["amazon"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Amazon.")
                    mia("J'ouvre Amazon.")
                    led_off()
                    bravepath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
                    wb.get(bravepath).open_new_tab("https://www.amazon.fr/")
                    fini = True
            for x in dico_apps["cdiscount"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Cdiscount.")
                    mia("J'ouvre Cdiscount.")
                    led_off()
                    bravepath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
                    wb.get(bravepath).open_new_tab("https://www.cdiscount.com/")
                    fini = True
            for x in dico_apps["twitch"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Twitch.")
                    mia("J'ouvre Twitch.")
                    led_off()
                    bravepath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s'
                    wb.get(bravepath).open_new_tab("https://www.twitch.tv/")
                    fini = True
            for x in dico_apps["camtasia"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre Camtasia.")
                    mia("J'ouvre Came tazia.")
                    led_off()
                    subprocess.Popen('C:/Program Files/TechSmith/Camtasia 2019/CamtasiaStudio.exe')
                    fini = True
            for x in dico_apps["jeux"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre le dossier de jeux.")
                    mia("J'ouvre le dossier de jeux.")
                    led_off()
                    path = 'D:/Users/Thibault/Documents/Documents/Jeux'
                    os.system(f'start {os.path.realpath(path)}')
                    fini = True
            for x in dico_apps["logiciels"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre le dossier de logiciels.")
                    mia("J'ouvre le dossier de logiciels.")
                    led_off()
                    path2 = 'D:/Users/Thibault/Documents/Documents/Logiciels'
                    os.system(f'start {os.path.realpath(path2)}')
                    fini = True
            for x in dico_apps["code"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre le dossier de code.")
                    mia("J'ouvre le dossier de code.")
                    led_off()
                    path = 'E:/Coding/GitHub'
                    os.system(f'start {os.path.realpath(path)}')
                    fini = True
            for x in dico_apps["bureau"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre le bureau.")
                    mia("J'ouvre le bureau.")
                    led_off()
                    path = 'C:/Users/Thibault/Desktop'
                    os.system(f'start {os.path.realpath(path)}')
                    fini = True
            for x in dico_apps["teams"]:
                if x in command.lower():
                    print("M.I.A : J'ouvre teams.")
                    mia("J'ouvre teams.")
                    led_off()
                    path = 'C:/Users/Thibault/AppData/Local/Microsoft/Teams/Update.exe'
                    os.system(f'start {os.path.realpath(path)}')
                    fini = True
            fini = True


# Fonction fermer M.I.A
def leave():
    print("M.I.A : Je m'éteins, au revoir boss.")
    mia("Je m'éteins, au revoir boss.")
    led_off()
    # quit()
    WMI = GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')

    for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
        print("Killing PID:", p.Properties_('ProcessId').Value)
        os.system("taskkill /pid "+str(p.Properties_('ProcessId').Value))


# Fonction qui donne la météo
def meteo(ville):
    # command = command.replace("mia donne moi la météo à", "")
    url_weather = "http://api.openweathermap.org/data/2.5/weather?q="+ville+"&APPID=beb97c1ce62559bba4e81e28de8be095"
    r_weather = requests.get(url_weather)
    data = r_weather.json()

    print("M.I.A : A " + ville)
    mia("A " + ville)
    led_off()
    #temperature moyenne
    t = data['main']['temp']
    t_moy = int(t-273.15)
    print(f"M.I.A : La température moyenne est de {t_moy} degrés Celsius")
    mia(f"La température moyenne est de {t_moy} degrés Celsius")
    led_off()
    #écart de température
    t_min = data['main']['temp_min']
    t_max = data['main']['temp_max']
    var1 = int(t_min-273.15)
    var2 = int(t_max-273.15)
    print(f"M.I.A : Les températures varient de {var1} à {var2} degrés Celsius")
    mia(f"Les températures varient de {var1} à {var2} degrés Celsius")
    led_off()
    #taux d'humidité
    humidite = data['main']['humidity']
    print("M.I.A : Le taux d'humidité est de {}".format(humidite) + "%")
    mia("Le taux d'humidité est de {}".format(humidite) + "%")
    led_off()
    #état du ciel 
    temps = data['weather'][0]['description']
    # output = trad.translate(temps)
    translate_temps = translator.translate(temps, lang_tgt='fr')
    print("M.I.A : Conditions climatiques : {}".format(translate_temps))
    mia("Conditions climatiques : {}".format(translate_temps))
    led_off()


# Fonction qui donne les décimales de pi
def pidec():
    """Calcul de pi avec la précision courante (méthode avec arc sinus)"""
    getcontext().prec += 2
    x = Decimal("0.5")

    xc = x*x
    k = x
    s1 = k
    n = 0

    while True:
        n += 1
        k *= xc*(2*n-1)*(2*n-1)/(2*n*(2*n+1))
        s2 = s1 + k
        
        if s2 == s1:
            break

        s1 = s2
        
    getcontext().prec -= 1
    return 6*s2


# Fonction du jeu "Le juste prix"
def juste_prix():
    number = random.randint(1, 100)
    tentatives = 8

    print(f"M.I.A : Ok, faisons un juste prix.\nM.I.A : Devinez un chiffre entre 1 et 100.\nM.I.A : Attention, vous n'avez que {tentatives} tentatives.")
    mia(f"Ok faisons un juste prix. Devinez un chiffre entre 1 et 100. Attention, vous n'avez que {tentatives} tentatives")
    led_off()

    while tentatives > 0:
        essai = take_command()
        if essai == "quitter":
            print("M.I.A : Vous avez quitter le jeu.")
            mia("Vous avez quitter le jeu.")
            led_off()
            break
        try:
            if int(essai) < number:
                print("M.I.A : C'est plus.")
                mia("C'est plusse.")
                led_off()
                tentatives -= 1
                if tentatives == 1:
                    print(f"M.I.A : Il vous reste {tentatives} tentative.")
                    mia(f"Il vous reste {tentatives} tentative.")
                    led_off()
                elif tentatives > 0:
                    print(f"M.I.A : Il vous reste {tentatives} tentatives.")
                    mia(f"Il vous reste {tentatives} tentatives.")
                    led_off()
            elif int(essai) > number:
                print("M.I.A : C'est moins.")
                mia("C'est moins.")
                led_off()
                tentatives -= 1
                if tentatives == 1:
                    print(f"M.I.A : Il vous reste {tentatives} tentative.")
                    mia(f"Il vous reste {tentatives} tentative.")
                    led_off()
                elif tentatives > 0:
                    print(f"M.I.A : Il vous reste {tentatives} tentatives.")
                    mia(f"Il vous reste {tentatives} tentatives.")
                    led_off()
            elif int(essai) == number:
                print(f"M.I.A : Félicitations boss, vous avez trouver le chiffre secret {number}.")
                mia(f"Félicitations boss, vous avez trouver le chiffre secret {number}.")
                led_off()
                break
            elif int(essai) > 100:
                print("M.I.A : Dites un chiffre entre 1 et 100.")
                mia("Dites un chiffre entre 1 et 100.")
                led_off()
        except ValueError:
            print("M.I.A : Dites un chiffre valide.")
            mia("Dites un chiffre valide")
            led_off()
        if tentatives == 0 and essai != number:
            print(f"M.I.A : Désolé boss, vous avez perdu le nombre à deviner était {number}.")
            mia(f"Désolé boss, vous avez perdu le nombre à deviner, était {number}.")
            led_off()


# Fonction qui donne les statistiques du coronavirus
def covid_stat():
    covid = Covid()
    cases = covid.get_status_by_country_name('France')
    active = covid.get_total_active_cases()
    confirmed = covid.get_total_confirmed_cases()
    recovered = covid.get_total_recovered()
    deaths = covid.get_total_deaths()

    print("M.I.A : France :")
    mia("En France")
    led_off()
    
    print(f"M.I.A : Nombre de cas actifs :     {active}")
    mia(f"Le nombre de cas actifs au covid est de {active}")
    led_off()
    
    print(f"M.I.A : Nombre de cas confirmés :  {confirmed}")
    mia(f"Le nombre de cas confirmés est de {confirmed}")
    led_off()

    print(f"M.I.A : Nombre de décès :          {deaths}")
    mia(f"Le nombre de décès au covid est de {deaths}")
    led_off()
    
    print(f"M.I.A : Nombre de cas guéris :     {recovered}")
    mia(f"Et le nombre de cas guéris dans le monde est de {recovered}")
    led_off()


# Fonction qui donne une suite de lettres aléatoires
def random_letter(length):
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(length)))
    return result_str


# Fonction qui fait un screenshot
def screenshot():
    img = pyautogui.screenshot()
    name_of_screen = random_letter(random.randint(10, 40)) + ".png"
    img.save(r"C:/Users/Thibault/Documents/mia/screenshots/" + name_of_screen)


# Fonction réveil
def alarm():
    print("M.I.A : A quelle heure voulez-vous mettre un réveil ?")
    mia("A quelle heure voulez-vous mettre un réveil ?")
    led_off()
    alarm_hour = take_command()
    now_hour = datetime.datetime.now().strftime("%Hh%M")
    print("M.I.A : Très bien, je mets un réveil à " + alarm_hour + ".")
    mia("Très bien, je mets un réveil à " + alarm_hour)
    led_off()
    song = AudioSegment.from_wav("Nickelback_-_How_You_Remind_Me.wav")

    test = True
    while test:
        now_hour = datetime.datetime.now().strftime("%Hh%M")

        if alarm_hour == now_hour:
            print("M.I.A : Réveillez-vous !")
            mia("Réveillez-vous !")
            led_off()
            play(song)
            while play(song):
                command = take_command().lower()
                if "mia stop" in command:
                    test = False
            break


# Fonction manger
def manger():
    print("M.I.A : Souhaitez-vous que je mette l'ordinateur en veille ?")
    mia("Souhaitez-vous que je mette l'ordinateur en veille ?")
    led_off()
    response = take_command()
    boucle = True
    while boucle:
        if "oui" in response:
            print("M.I.A : Je met l'ordinateur en veille.\nM.I.A : Bon appétit boss.")
            mia("Je mets l'ordinateur en veille. Bonne appétit boss.")
            led_off()
            boucle = False
            os.system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')
        elif "non" in response:
            print("Ca marche. Bon appétit boss.")
            mia("Ca marche. Bonne appétit boss.")
            led_off()                        
            boucle = False
        else:
            print("M.I.A : Souaitez-vous que je mette l'ordinateur en veille ?")
            mia("Souaitez-vous que je mette l'ordinateur en veille ?")
            led_off()


# Fonction horoscope
def zodiac():

    print("Bélier\nTaureau\nGémeaux\nCancer\nLion\nVierge\nBalance\nScorpion\nSagitaire\nCapricorne\nVerseau\nPoisson\n")

    while True:
        print("M.I.A : Quel horoscope voulez-vous savoir ?")
        mia("Quel horoscope voulez-vous savoir ?")
        led_off()

        french_sign = take_command()

        if "bélier" in french_sign:
            french_sign = "Bélier"
            sign = "Aries"
            break
        elif "taureau" in french_sign:
            french_sign = "Taureau"
            sign = "Taurus"
            break
        elif "Gémo" in french_sign:
            french_sign = "Gémeaux"
            sign = "Gemini"
            break
        elif "cancer" in french_sign:
            french_sign = "Cancer"
            sign = "Cancer"
            break
        elif "Lyon" in french_sign:
            french_sign = "Lion"
            sign = "Leo"
            break
        elif "vierge" in french_sign:
            french_sign = "Vierge"
            sign = "Virgo"
            break
        elif "balance" in french_sign:
            french_sign = "Balance"
            sign = "Libra"
            break
        elif "Scorpion" in french_sign:
            french_sign = "Scorpion"
            sign = "Scorpio"
            break
        elif "Sagittaire" in french_sign:
            french_sign = "Sagittaire"
            sign = "Sagittarus"
            break
        elif "Capricorne" in french_sign:
            french_sign = "Capricorne"
            sign = "Capricorn"
            break
        elif "Verseau" in french_sign:
            french_sign = "Verseau"
            sign = "Aquarius"
            break
        elif "poisson" in french_sign:
            french_sign = "Poisson"
            sign = "Pisces"
            break
        else:
            print("M.I.A : Dites un signe astrologique valide.")
            mia("Dites un signe astrologique valide.")
            led_off()

    while True:
        print("M.I.A : Vous voulez l'horoscope d'hier, aujourd'hui ou demain ?")
        mia("Vous voulez l'horoscope d'hier, aujourd'hui ou demain ?")
        led_off()

        french_day = take_command()

        if "hier" in french_day:
            day = "Yesterday"
            break
        elif "aujourd'hui" in french_day:
            day = "Today"
            break
        elif "demain" in french_day:
            day = "Tomorrow"
            break
        else:
            print("M.I.A : Dites un jour valide.")
            mia("Dites un jour valide")
            led_off()

    params = (

        ('sign', sign),
        ('day', day)

        )

    response = requests.post('https://aztro.sameerkumar.website/', params=params)
    json = response.json()

    translate_date = translator.translate(json.get('current_date'), lang_tgt='fr')
    print("M.I.A : L'horoscope du", translate_date)
    mia("L'horoscope du " + translate_date)
    led_off()

    print("M.I.A : " + french_sign)
    mia(french_sign)
    led_off()

    translate_description = translator.translate(json.get('description'), lang_tgt='fr')
    print("M.I.A : " + translate_description)
    mia(translate_description)
    led_off()

    translate_compatibility = translator.translate(json.get('compatibility'), lang_tgt='fr')
    print("M.I.A : Vous êtes compatible avec", translate_compatibility)
    mia("Vous êtes compatible avec " + translate_compatibility)
    led_off()

    translate_color = translator.translate(json.get('color'), lang_tgt='fr')
    print("M.I.A : Votre couleur est le", str(translate_color[0]))
    mia("Votre couleur est le " + str(translate_color[0]))
    led_off()

    translate_lucky_number = translator.translate(json.get('lucky_number'), lang_tgt='fr')
    print("M.I.A : Et votre chiffre porte bonheur est le", translate_lucky_number)
    mia("Et votre chiffre porte bonheur est le " + translate_lucky_number)
    led_off()


# Fonction google maps
def maps(location):
    print("M.I.A : Je vous affiche la location de " + location + ".")
    mia("Je vous affiche la location de " + location)
    led_off()
    webbrowser.open("https://www.google.com/maps/place/" + location + "")


# Fonction qui calcul
def calcul(my_string):
    def get_operator_fn(op):
        return {
            '+' : operator.add,
            '-' : operator.sub,
            'x' : operator.mul,
            '/' :operator.__truediv__,
            'divisé par' :operator.__truediv__,
            'mod' : operator.mod,
            'modulo' : operator.mod,
            'Mod' : operator.mod,
            'Modulo' : operator.mod,
            '^' : operator.xor,
            'puissance' : operator.xor,
        }[op]


    def eval_binary_expr(op1, oper, op2):
        op1,op2 = int(op1), int(op2)
        return get_operator_fn(oper)(op1, op2)


    print(eval_binary_expr(*(my_string.split())))








# [---------- MAIN ----------]

if __name__ == "__main__":
    led_off()
    if not reco_fac():

        time.sleep(1.5)

        print("\n")
        premier()

        while True:
            command = take_command().lower()
# 
            if "merci mia" in command:
                print("M.I.A : De rien boss.")
                mia("De rien boss.")
                led_off()
# 
            elif "mia" in command or "milla" in command:
# 
                if "heure" in command:
                    print("M.I.A : Il est " + time_hour() +".")
                    mia("Il est " + time_hour())
                    led_off()
# 
                elif "quel jour" in command or "date" in command:
                    print("M.I.A : On est le " + date() + ".")
                    mia("On est le " + date())
                    led_off()

                elif "arduino" in command:
                    arduino_control()

                elif "montre-moi ton code" in command or "montrer ton code" in command or "montre ton code" in command:
                    print("M.I.A : J'ouvre mon dossier de code.")
                    mia("J'ouvre mon dossier de code.")
                    led_off()
                    path = 'C:/Users/Thibault/Documents/mia'
                    os.system(f'start {os.path.realpath(path)}')
#
                elif "ça va" in command or "comment vas-tu" in command or "comment tu vas" in command or "bien ou quoi" in command:
                    current_feeling = ["Je vais bien ", "Tranquille "]
                    feeling = random.choice(current_feeling)
                    print("M.I.A : " + feeling + "merci. Et vous ?")
                    mia(feeling + "merci. Et vous ?")
                    led_off()
# 
                elif "présente-toi" in command or "présenter" in command:
                    print("Je suis M.I.A, l'intelligence artificielle de Thibault.")
                    mia("Je suis Mia, l'intelligence artificielle de Thibault")
                    led_off()
# 
                elif "bête" in command or "moche" in command or "idiote" in command or "laide" in command or "conne" in command or "inutile" in command or "sers à rien" in command or "merde" in command or "nul" in command:
                    current_response = ["Je ne me permettrai pas d'arriver à votre niveau", 
                                        "Tout comme vous boss", 
                                        "Merci bien vous aussi", 
                                        "La vérité sort de la bouche des enfants boss.", 
                                        "Vous n'êtes vraiment pas très sympa, mais le train de vos injures roule sur le rail de mon indifférence, Boss.", 
                                        "Vous habitez en face du cimetière mais dans un avenir proche vous habiterai en face de chez vous.", 
                                        "Vous cherchez l'ambiance ou l'ambulance ?"]
                    response = random.choice(current_response)
                    print("M.I.A : " + response)
                    mia(response)
                    led_off()
# 
                elif "je t'aime" in command:
                    print("M.I.A : Tu drevrais sortir voir le monde, fréro.")
                    mia("Tu devrais sortir voir le monde, fréro.")
                    led_off()

                elif "qui est" in command:
                    command = command.replace("mia qui est", "")
                    print("Voici ce que j'ai trouvé sur Wikipédia.")
                    mia("Voici ce que j'ai trouvé sur Wikipédia.")
                    led_off()
                    translate_text = translator.translate(wikipedia.summary(command, sentences=2),lang_tgt='fr')
                    print("M.I.A : " + translate_text)
                    mia(translate_text)
                    led_off()
# 
                elif "cherche" in command and "google" in command:
                    print("M.I.A : Voici ce que j'ai trouvé sur internet.")
                    mia("Voici ce que j'ai trouvé sur internet.")
                    led_off()
                    command = command.replace("mia cherche sur google", "")
                    if "photo" in command or "image" in command:
                        wb.open("https://www.google.com/search?tbm=isch&q={}".format(command))
                    else:
                        wb.open("https://www.google.com/search?q={}".format(command))
# 
                elif "cherche" in command and "youtube" in command:
                    print("M.I.A : Voici ce que j'ai trouvé sur YouTube.")
                    mia("Voici ce que j'ai trouvé sur You tube.")
                    led_off()
                    command = command.replace("mia cherche sur youtube", "")
                    wb.open("https://www.youtube.com/search?q={}".format(command))
# 
                elif "ouvre" in command:
                    command = command.replace("mia ouvre", "")
                    application(command)
# 
                elif "lance" in command:
                    command = command.replace("mia lance ", "")
                    application(command)
                
                elif "météo" in command:
                    print("M.I.A : Vous voulez la météo de quelle ville boss ?")
                    mia("Vous voulez la météo de quelle ville boss ?")
                    led_off()
                    ville = take_command()
                    meteo(ville)

                elif "pile ou face" in command:
                    coin = ["Pile", "Face"]
                    random_coin = random.choice(coin)
                    print("M.I.A : Je lance la pièce.")
                    mia("Je lance la pièce.")
                    led_off()
                    print("M.I.A : C'est " + random_coin + ".") 
                    mia("C'est " + random_coin)
                    led_off()

                elif "décimales" in command and "pi" in command:
                    print("M.I.A : Combien de décimales de Pi voulez-vous ?")
                    mia("Combien de décimales de Pi voulez-vous ?")
                    led_off()
                    while True:
                        try:
                            getcontext().prec = int(take_command())
                            if getcontext().prec > 150:
                                print("M.I.A : Désolé boss mais j'ai la flemme de dire autant de chiffres à la suite.")
                                mia("Désolé boss mais j'ai la flemme de dire autant de chiffres à la suite.")
                                led_off()
                                break
                            else:
                                print("M.I.A : Pi c'est " + str(pidec()))
                                mia("Pi c'est " + str(pidec()))
                                led_off()
                                break
                        except ValueError:
                            print("M.I.A : Désolé j'attends un nombre valide.")
                            mia("Désolé j'attends un nombre valide.")
                            led_off()

                elif "juste prix" in command:
                    juste_prix()

                # A MODIFIER 
                elif "Noël" in command or "noël" in command:
                    christmas()

                # A MODIFIER
                elif "Nouvel An" in command or "nouvel an" in command:
                    newYear()

                # A MODIFIER
                elif "anniversaire" in command:
                    birthday()

                elif "dis bonjour" in command:
                    command = command.replace("mia dis bonjour à ", "")
                    if command == "papa":
                        print("M.I.A : Bonjour le papa du boss. Comment allez-vous ?")
                        mia("Bonjour le papa du boss. Comment tallé vous ?")
                        led_off()
                    elif command == "maman":
                        print("M.I.A : Bonjour la maman du boss. Comment allez-vous ?")
                        mia("Bonjour la maman du boss. Comment tallé vous ?")
                        led_off()
                    elif command == "salomé":
                        print("M.I.A : Bonjour la copine du boss. Comment allez-vous ?")
                        mia("Bonjour la copine du boss. Comment tallé vous ?")
                        led_off()
                    elif command == "martin":
                        print("M.I.A : Wesh gros, tranquille ou quoi ?")
                        mia("Wesh gros, tranquille ou quoi ?")
                        led_off()
                    elif command == "océane":
                        print("M.I.A : Bonjour, euh c'est comment déjà ? Je sais plus, bon, bonjour machin.")
                        mia("Bonjour. Euh c'est comment déjà ? Je sais plus. Bon. Bonjour machin.")
                        led_off()
                    elif command == "la team algérienne":
                        print("M.I.A : Salam aleykoum les khouya.")
                        mia("Salamalékoum les rouya.")
                        led_off()
                    else:
                        print("M.I.A : Bonjour" + command + ". Comment allez-vous ?")
                        mia("Bonjour " + command + ". Comment tallé vous ?")
                        led_off()

                elif "mets un rappel" in command or "mettre un rappel" in command:
                    command = command.replace("mia mets un rappel ", "")
                    with open('reminder.txt', 'a') as f:
                        f.write(date() + " à " + time_hour() + " : ")
                        f.write(command)
                        print("M.I.A : Je vous ai mis le rappel " + command + ".")
                        mia("Je vous ai mis le rappel " + command + ".")
                        led_off()

                elif "lire mes rappels" in command:
                    with open('reminder.txt', 'r') as f:
                        content = f.read()
                        if content == '':
                            print("M.I.A : Vous n'avez aucun rappel.")
                            mia("Vous n'avez aucun rappel.")
                            led_off()
                        else:
                            print("M.I.A : " + content + ".")
                            mia(content)
                            led_off()
                    
                # elif "efface mes rappels du" in command:
                #     command = command.replace("mia efface mes rappels du ", "")

                #     for date in command:
                #         with open('reminder.txt', 'w') as f:
                #             f.write('')
                #     print("M.I.A : J'ai effacé vos rappels du " + command + ".")
                #     mia("J'ai effacé vos rappels du " + command + ".")

                elif "efface tous mes rappels" in command or "effacer tous mes rappels" in command:
                    print("M.I.A : J'ai effacé tous vos rappels.")
                    mia("J'ai effacé tous vos rappels.")
                    led_off()
                    with open('reminder.txt', 'w') as f:
                        f.write('')

                elif "j'ai perdu" in command:
                    print("M.I.A : Cheh.")
                    mia("Cheh.")
                    led_off()
# 
                elif "tu sers à quoi" in command:
                    print("M.I.A : Tout comme vous boss, à pas grand chose.")
                    mia("Tout comme vous boss, à pas grand chose.")
                    led_off()

                elif "infosystem" in command or ("informations" in command and "système" in command):
                    info_sys()

                elif "coronavirus" in command or "covid" in command or "COVID-19" in command:
                    covid_stat()

                elif "screenshot" in command:
                    print("M.I.A : J'ai fais un screenshot.")
                    mia("J'ai fais un screenshot")
                    led_off()
                    screenshot()

                elif "réveil" in command:
                    alarm()

                elif "horoscope" in command:
                    zodiac()
                
                elif "dit" in command:
                    command = command.replace("mia dit ", "")
                    print("M.I.A : " + command)
                    mia(command)
                    led_off()

                elif "température" in command:
                    activate_temperature()

                elif "où est" in command:
                    command = command.replace("mia où est ", "")
                    location = command
                    maps(location)

                elif "c'est où" in command:
                    command = command.replace("mia c'est où ", "")
                    location = command
                    maps(location)

                elif "calcul" in command:
                    my_string = command.replace("mia calcul ", "")
                    my_string_en = translator.translate(my_string, lang_tgt='en')
                    calcul(my_string_en)
                    # print("M.I.A : " + str(my_string) + " = " + str(calcul(my_string_en)))
                    # mia(str(my_string) + " est égal à " + str(calcul(my_string_en)))
                    # led_off()

                elif ("vide" in command or "vider" in command) and "corbeille" in command:
                    winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
                    print("M.I.A : J'ai vidé la corbeille.")
                    mia("J'ai vidé la corbeille.")
                    led_off()

                elif "je vais manger" in command:
                    manger()

                elif "chut" in command or "muet" in command or "parle" in command:
                    volume_mute()

                elif ("monte" in command or "augmente" in command) and "son" in command:
                    for i in range(0, 10):
                        volume_up()

                elif ("baisse" in command or "diminue" in command) and "son" in command:
                    for i in range(0, 10):
                        volume_down()

                elif "son" in command and ("max" in command or "fond" in command):
                    set_volume(100)

                elif "son" in command and ("minimum" in command or "plus bas" in command):
                    set_volume(0)

                elif "mets" in command and "son" in command:
                    command = command.replace("mia mets le son à ", "")
                    amount = int(command)
                    set_volume(amount)

                elif "clear" in command:
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif "casse-toi" in command or "va-t'en" in command:
                    leave()

                elif ("éteins" in command or "éteindre" in command) and "ordinateur" in command:
                    print("M.I.A : J'éteins l'ordinateur.")
                    mia("J'éteins l'ordinateur.")
                    led_off()
                    os.system("shutdown /s /t 1")
                
                elif "veille" in command:
                    os.system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')
                
                elif ("redémarre" in command or "redémarrer" in command) and "ordinateur" in command:
                    print("M.I.A : Je redémarre l'ordinateur.")
                    mia("Je redémarre l'ordinateur.")
                    led_off()
                    os.system("shutdown /r /t 1")
# 
                else:
                    print("M.I.A : Désolé boss, je ne suis pas encore capable de faire cela.")
                    mia("Désolé boss, je ne suis pas encore capable de faire cela.")
                    led_off()

            else:
                pass
                # do_nothing()