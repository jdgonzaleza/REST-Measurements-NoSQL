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

# Create your views here.


