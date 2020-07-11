from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Utilities.utilities import *
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.utils import json


@api_view(['POST'])
def get_movie_list(request):
    final_list = {'ok': True, "data": []}
    if request.method == 'POST':
        data = request.data
        ml = MovieList(data['movies'], data['data_format'])
        final_list['data'] = ml.final_list

    return JsonResponse(final_list, status=status.HTTP_200_OK,safe=False)
