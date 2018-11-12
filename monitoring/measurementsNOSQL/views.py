from django.shortcuts import render
from rest_framework import (response, schemas, filters, generics, viewsets,
                        views)
from django.http import JsonResponse
from pymongo import MongoClient
import datetime
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.generics import GenericAPIView
from django.conf import settings
from bson import Binary
from bson.json_util import dumps
import time
import datetime

# Create your views here.

@api_view(["GET", "POST"])
def variables(request):
    client = MongoClient(settings.DB_HOST, int(settings.DB_PORT))
    db = client[settings.MONGO_DB]
    db.authenticate(settings.MLAB_USER, settings.MLAB_PASSWORD)
    variables = db['variables']
    if request.method == "GET":
        result = []
        data = variables.find({})
        for dto in data:
            jsonData = {
                'id': str(dto['_id']),
                "idBusqueda": dto["idBusqueda"],
                "variable": dto['variable'],
                'threshold': dto['threshold']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        idBusqueda = int((time.time()*1000) % 86400000)
        data['idBusqueda'] = idBusqueda
        result = variables.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)

@api_view(["GET", "POST"])
def variablesDetail(request, pk):
    client = MongoClient(settings.DB_HOST, int(settings.DB_PORT))
    db = client[settings.MONGO_DB]
    db.authenticate(settings.MLAB_USER, settings.MLAB_PASSWORD)
    variables = db['variables']
    if request.method == "GET":
        data = variables.find({'idBusqueda': int(pk)})
        result = []
        for dto in data:
            jsonData ={
                'id': str(dto['_id']),
                "variable": dto['variable'],
                'threshold': dto['threshold']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result[0], safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)
        result = variables.update(
            {'idBusqueda': int(pk)},
            {'$push': {'threshold': data}}
        )
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        return JsonResponse(respo, safe=False)

        
          
@api_view(["GET", "POST"])
def lugar(request):
    client = MongoClient(settings.DB_HOST, int(settings.DB_PORT))
    db = client[settings.MONGO_DB]
    db.authenticate(settings.MLAB_USER, settings.MLAB_PASSWORD)
    lugar = db['lugar']
    if request.method == "GET":
        result = []
        data = lugar.find({})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "lugar": dto['lugar'],
                "idBusqueda": dto['idBusqueda'],
                'variable': dto['variable'],
                'measurements': dto['measurements'],
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)
        measurements = []
        idBusqueda = int((time.time()*1000) % 86400000)
        data['idBusqueda']= idBusqueda
        data['measurements'] = measurements
        result = lugar.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)

@api_view(["GET", "POST", "DELETE"])
def lugarDetail(request, pk):
    client = MongoClient(settings.DB_HOST, int(settings.DB_PORT))
    db = client[settings.MONGO_DB]
    db.authenticate(settings.MLAB_USER, settings.MLAB_PASSWORD)
    lugar = db['lugar']
    if request.method == "GET":
        result = []
        data = lugar.find({'idBusqueda': int(pk)})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "lugar": dto['lugar'],
                "idBusqueda": dto['idBusqueda'],
                'variable': dto['variable'],
                'measurements': dto['measurements'],
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result[0], safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)
        elTiempo = time.gmtime()
        laFecha = time.strftime("%Y-%m-%d %H:%M:%S",elTiempo) 
        elSplit = laFecha.split(" ")
        data['date']= elSplit[0]
        data['time']= elSplit[1]
        result = lugar.update(
            {'idBusqueda': int(pk)},
            {'$push': {'measurements': data}}
        )
        respo = {
            "MongoObjectID": str(result),
            "Mensaje": "Se añadió una nueva medida"
        }
        client.close()
        return JsonResponse(respo, safe=False)
    if request.method == "DELETE":
        result = lugar.remove({"idBusqueda": int(pk)})
        respo = {
            "MongoObjectID": str(result),
            "Mensaje": "Se ha borrado un lugar"
        }
        client.close()
        return JsonResponse(respo, safe=False)

@api_view(["GET", "POST"])
def alerta(request):
    client = MongoClient(settings.DB_HOST, int(settings.DB_PORT))
    db = client[settings.MONGO_DB]
    db.authenticate(settings.MLAB_USER, settings.MLAB_PASSWORD)
    alerta = db['alerta']
    if request.method == "GET":
        result = []
        data = alerta.find({})
        for dto in data:
            jsonData ={
                "idBusqueda": dto["idBusqueda"],
                "place": dto['place'],
                "date": dto['date']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        idBusqueda = int((time.time()*1000) % 86400000)
        elTiempo = time.gmtime()
        laFecha = time.strftime("%Y-%m-%d %H:%M:%S",elTiempo)        
        data['idBusqueda'] =idBusqueda
        data['date']= laFecha
        result = alerta.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)

@api_view(["GET"])
def alertaDetail(request, pk):
    client = MongoClient(settings.DB_HOST, int(settings.DB_PORT))
    db = client[settings.MONGO_DB]
    db.authenticate(settings.MLAB_USER, settings.MLAB_PASSWORD)
    alerta = db['alerta']
    data = alerta.find({'idBusqueda': int(pk)})
    result = []
    for dto in data:
        jsonData ={
            "idBusqueda": dto["idBusqueda"],
            "place": dto['place'],
            "date": dto['date']
        }
        result.append(jsonData)
    client.close()
    return JsonResponse(result[0], safe=False)








    