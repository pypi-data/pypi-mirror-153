#Libreria
from tkinter import * 
import pyrebase
import random
import time 
from datetime import datetime
from email.message import EmailMessage
import Adafruit_DHT as dht
#import smtplib
import RPi.GPIO as GPIO #libreria para prender y apagar la raspberry
import os
# Parametro para DHT
sensor = dht.DHT22

# Firebase Configuracion de conexion
firebaseConfig = {
    "apiKey": "AIzaSyCrtUk2_VcrjxMOSqfZJz61cJ-tER0p7CU",
    "authDomain": "bioterio-34fd4.firebaseapp.com",
    "databaseURL": "https://bioterio-34fd4-default-rtdb.firebaseio.com",
    "projectId": "bioterio-34fd4",
    "storageBucket": "bioterio-34fd4.appspot.com",
    "messagingSenderId": "247706174495",
    "appId": "1:247706174495:web:210c416fcdbdde4cc2b34a"
};
firebase=pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
def medicion(TempSen):
    if TempSen == "SimulSegundero":

        result = time.localtime()
        # Tsensada = 4 con esto veo que el retraso se debe al tiempo en correr el sensado o la linea de abajo

        Tsensada = result.tm_sec #PARA TEMPERATURA DE SIMULACION SEG
        db.child("SimulSegunderoTemperaturaActual").update({"Temperatura": Tsensada})
        Hsensada = -1 # lo pongo para q desp no tire error en caso de usar el simulSegundero al no estar definida Hsensada

                
    elif TempSen == "Bioterio":

         Hbioterio,Tbioterio = dht.read_retry(sensor,4)
         

         Hsensada = round(Hbioterio,2)
         print(Hsensada)

         Tsensada = round(Tbioterio,2) #RECIBO T SENSOR BIOTERIO

         db.child("BioterioHumedadActual").update({"Humedad": Hsensada})
         db.child("BioterioTemperaturaActual").update({"Temperatura": Tsensada})         

    return [Tsensada,Hsensada]

def promedio(Tsensada,Hsensada,TempSen,Intervalo,contador,TsensadaAcumulada,HsensadaAcumulada,tpoInicialPromedio):
    TsensadaAcumulada = TsensadaAcumulada + Tsensada
    HsensadaAcumulada = HsensadaAcumulada + Hsensada

    Tpromedio = TsensadaAcumulada / contador
    Hpromedio = HsensadaAcumulada / contador
                        
    tpoFinalPromedio = datetime.now()

    delayPromedio =  tpoFinalPromedio - tpoInicialPromedio

    if delayPromedio.seconds > Intervalo: #este es el intervalo de tiempo en el que toma el promedio de Temps o Hums

        contador = 0
        TsensadaAcumulada = 0
        HsensadaAcumulada = 0
        # print(Tpromedio)
        tpoInicialPromedio = datetime.now()


        if TempSen == "Bioterio":
            db.child("BioterioTemperaturaRegistro").push({"Temperatura": round(Tpromedio,2), "Date" : datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")})
            db.child("BioterioHumedadRegistro").push({"Humedad": round(Hpromedio,2), "Date" : datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")})

        
        elif TempSen == "SimulSegundero":
            db.child("SimulSegunderoTemperaturaRegistro").push({"Temperatura": round(Tpromedio,2), "Date" : datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")})

def Alarma(Tsensada,tempSensor,Hsensada):
    dateTimeObj=datetime.now()

    fecha = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)") #ojo aca la hora que toma

    alert={"TempAlerta":Tsensada,'Date': fecha}
    alertConHum={"TempAlerta":Tsensada,'Date': fecha, 'HumAlerta': Hsensada}

    if tempSensor == "SimulSegundero" or tempSensor == "SimulPulso":
        db.child("SimulSegunderoAlertaRegistro").push(alert)

    elif tempSensor == "Bioterio":
        db.child("BioterioAlertaRegistro").push(alertConHum)
    return fecha
