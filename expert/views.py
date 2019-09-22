import json
import os

import pandas as pd
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render_to_response
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def get_data(well=None):
    data = [
        {
            'percent': 0.72,
            'labs': [  # Исследования
                {
                    'value': 'A',
                },
                {
                    'value': 'B',
                },
                {
                    'value': 'C',
                },
            ],
            'height': 100  # Метры длинны
        },
        {
            'percent': 0.5,
            'labs': [ # Исследования
                {
                    'value': 'B'
                },
                {
                    'value': 'C'
                }
            ],
            'height': 30  # Метры длинны
        },
        {
            'percent': 0.25,
            'labs': [  # Исследования
                {
                    'value': 'A'
                }
            ],
            'height': 40  # Метры длинны
        }
    ]

    h = 1  # метров нефти
    exp = 45000000  # цена за исследования
    cost = (h * 0.7 * 100 * 860 * 4150)
    searchs = {
        'data': [
            {
                'name': 'BK',
                'count': 4,
                'cost': 2450,
                'y': 4 * 2450
            },
            {
                'name': 'GZ(1-7)',
                'count': 2,
                'cost': 2050,
                'y': 4 * 2050
            },
            {
                'name': 'DGK',
                'count': 7,
                'cost': 1300,
                'y': 4 * 1300
            },
            {
                'name': 'NKT(D/M/R)',
                'count': 8,
                'cost': 2050,
                'y': 4 * 2050
            },
            {
                'name': 'ALPS',
                'count': 3,
                'cost': 1150,
                'y': 4 * 1150
            }
        ],
        'allSum': exp
    }

    return data, searchs, cost, exp, h  # чет много параметров


def index(request):
    well = 1
    if 'well' in request.GET and request.GET['well']:
        well = request.GET['well']

    data, searchs, cost, exp, h = get_data(well)

    context = {
        'data': data,
        'jsonSearch': json.dumps(searchs['data']),
        'searchs': searchs,
        'profitCost': '{0:,}'.format(int(cost)).replace(",", " "),
        'profitСostDollar': '{0:,}'.format(int(cost / 64)).replace(",", " "),
        'cost': '{0:,}'.format(int(cost - exp)).replace(",", " "),
        'costDollar': '{0:,}'.format(int((cost - exp) / 64)).replace(",", " "),
        'exp': '{0:,}'.format(int(exp)).replace(",", " "),
        'expDollar': '{0:,}'.format(int(exp / 64)).replace(",", " "),
        'height': h,
        'OilPrice': 4150,
        'type': 'SAND'

    }
    return render_to_response('expert/index.html', context)


def handle_uploaded_file(f):
    with open('tmp/test.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@csrf_exempt
def load(request):
    context = {}
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'])

    return render_to_response('expert/load.html', context)
