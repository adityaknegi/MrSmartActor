from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Utilities.utilities import *
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.utils import json


@api_view(['POST'])
def get_one_movies_list(request):
    final_list = {"total_money": str(0)+' crore', "data": []}

    if request.method == 'POST':
        data = dict(request.data)
        ml = MovieList(data['movies'], data['data_format'])
        final_list['data'] = ml.final_list
        final_list['total_money'] = str(len(ml.final_list)) + ' crore'

        return JsonResponse(final_list, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(final_list, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(['POST'])
def get_movies_set(request):
    final_list = {"total_money": str(0)+' crore', "options": 0,"data": []}

    if request.method == 'POST':
        data = request.data
        movies = request.POST.get('movie', None)
        data_format = request.POST.get('data_format', None)
        ml = MovieList(movies, data_format)
        max_len = len(ml.final_list)

        ml = MoviesListSET(movies, data_format, max_len)
        ml.movies_list()
        final_list['data'] = ml.final_movies_list
        final_list['total_money'] = str(len(ml.final_movies_list[0])) + ' crore'
        final_list['options'] = len(ml.final_movies_list)

        return JsonResponse(final_list, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(final_list, status=status.HTTP_400_BAD_REQUEST, safe=False)