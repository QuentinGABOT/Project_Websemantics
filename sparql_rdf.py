# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 16:35:23 2021

"""
import numpy as np
import rdflib
from pyowm import OWM
g = rdflib.Graph()
g.parse("Station_de_Velo.owl")

def calcul(city):
    ville = "'" + city + "'"
    print(ville)
    station = g.query(
        """
    SELECT DISTINCT  ?station 
       WHERE {
         ?a schema:City""" + ville+"""^^xsd:string .
         ?a schema:name ?station .
       }""")
    for row in station:
        print(row[0])
    print("selectionner une première station")
    name_station=input()
    stop=0
    while(stop==0):
        for row in station:
            if str(row[0]) == name_station:
                 stop=1
        if stop==0:
            print("selectionner une première station")
            name_station = input()
    name_1 = name_station
    name1 = "'" + name_station + "'"
    
    print("selectionner une deuxième station")
    name_station=input()
    stop=0
    while(stop==0):
        for row in station:
            if str(row[0]) == name_station:
                 stop=1
        if stop==0:
            print("selectionner une deuxième station")
            name_station = input()
    name_2 = name_station
    name2 = "'" + name_station + "'"
    
    lonlat1 = g.query(
    """
   
    SELECT DISTINCT   ?longitude ?latitude
       WHERE {
         ?a schema:City""" + ville+"""^^xsd:string .
         ?a schema:name""" +name1+"""^^xsd:string .
         ?a  schema:latitude ?latitude .
         ?a  schema:longitude ?longitude .
       }""")
    for row in lonlat1:
        lon1 = float(row[0])
        lat1 = float(row[1])
        
    lonlat2 = g.query(
    """
   
    SELECT DISTINCT   ?longitude ?latitude
       WHERE {
         ?a schema:City""" + ville+"""^^xsd:string .
         ?a schema:name""" +name2+"""^^xsd:string .
         ?a  schema:latitude ?latitude .
         ?a  schema:longitude ?longitude .
       }""")
    for row in lonlat2:
        lon2 = float(row[0])
        lat2 = float(row[1])
    #print(lon1,lon2,lat1,lat2)
    distance = calcul_distance(lon1,lon2,lat1,lat2)
    print("la distance entre " + name_1 + " et " + name_2 + "est de :" + str(distance) + "km")
    
    #print("la distance entre" + name1 + "et " + name2 + "est de "+ distance)
    return calcul_distance(lon1,lon2,lat1,lat2)
    
    

def calcul_distance(lon1,lon2,lat1,lat2):
    lon1=lon1*np.pi/180
    lon2=lon2*np.pi/180
    lat1=lon1*np.pi/180
    lat2=lon2*np.pi/180
    R = 6371
    phi = (lat2-lat1)
    theta = (lon2-lon1)
    a = np.sin(phi/2) * np.sin(phi/2) + np.cos(lat1) * np.cos(lat2) * np.sin(theta/2) * np.sin(theta/2)
    c = 2 * np.arctan2(np.sqrt(a),np.sqrt(1-a))
    d = R * c
    return d

def liste(city):
    ville = "'" + city + "'"
    qres = g.query(
        """
       
        SELECT DISTINCT  ?name ?velo
           WHERE {
             ?a schema:City""" + ville+"""^^xsd:string .
             ?a schema:name ?name .
             ?a :VelosLibres ?velo .
             FILTER( ?velo > 0) .
           }""")
    
    
    
    for row in qres:
        if(int(row[1])>0):
            print(row[0] + "à " + row[1] + " vélo libre")
      
def info(city):
    ville = "'" + city + "'"
    print(ville)
    station = g.query(
        """
    SELECT DISTINCT  ?station 
       WHERE {
         ?a schema:City""" + ville+"""^^xsd:string .
         ?a schema:name ?station .
       }""")
    for row in station:
        print(row[0])
    print("selectionner une station")
    name_station=input()
    stop=0
    while(stop==0):
        for row in station:
            if str(row[0]) == name_station:
                 stop=1
        if stop==0:
            print("selectionner une station")
            name_station = input()
            
    name = "'" + name_station + "'"
    
    qres = g.query(
    """
    SELECT DISTINCT  ?velo ?place
       WHERE {
         ?a schema:City""" + ville+"""^^xsd:string .
         ?a schema:name""" + name+ """^^xsd:string .
         ?a :VelosLibres ?velo .
         ?a :PlacesOccupees ?place .
       }""")

    for row in qres:
        print("il y a " + str(row[0]) + " velo libres")
        print("il y a " + str(row[1]) + " place occupés")
    

def meteo(city):
    owm = OWM('16a5487fc4d8dac9ce046806a59978ec')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather
    print("la température à " + city + " est de:")
    print( w.temperature('celsius')['temp'])
    
def getville():
    city = g.query(
    """
   
    SELECT DISTINCT  ?city
       WHERE {
         ?a schema:City ?city .
       }""")
    for row in city:
        print(row[0])
    print("selectionner une ville")
    name_city = input()
    stop=0
    while(stop==0):
        for row in city:
            if str(row[0]) == name_city:
                 stop=1
        if(stop==0):
            print("selectionner une ville")
            name_city = input()
    return name_city
        


if __name__ == "__main__":
    city = getville()
    print("Que voulez vous faire?")
    print("1 - Météo de la ville")
    print("2 - Information sur les stations vélos de la ville")
    
    number = int(input())
    
    if (number == 1):
        meteo(city)
    if (number == 2):
        
        print('Que voulez vous faire?')
        print('1 - Informations sur une station de vélo')
        print('2 - Distance entre 2 stations de vélo')
        print("3 - Liste des stations de vélo avec au moins 1 vélo")
        number = int(input())
        if(number==1):
            info(city)
        if(number==2):
            calcul(city)
        if(number==3):
            liste(city)
        
    
    
    
    