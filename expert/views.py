import json

import pandas as pd
from django.shortcuts import render_to_response
import numpy
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

data = pd.read_excel('tmp/test.xlsx')


def find_depth_of_oil(new_df, number_of_well):
    min_depth = new_df.groupby('well id')['depth, m'].min()
    max_depth = new_df.groupby('well id')['depth, m'].max()
    depth = max_depth - min_depth
    perc_of_oil = new_df.groupby('well id')['goal'].mean()
    depth_of_oil = perc_of_oil * depth
    df = depth_of_oil.reset_index().rename(columns = {0:'depth_of_oil'})
    return df[df['well id'] == int(number_of_well)].iloc[0,1]


def find_depth_of_well(df, number_of_well):
    max_depth = df.groupby('well id')['depth, m'].max()
    min_depth = df.groupby('well id')['depth, m'].min()
    depth = max_depth - min_depth
    depth = depth.reset_index()
    return depth[depth['well id'] == int(number_of_well)].iloc[0, 1]


def count_financial_model_all(depth_of_oil, depth_of_well):
    price_bk = 2450
    price_gz1 = 2050
    price_gz2 = 2050
    price_gz3 = 2050
    price_gz4 = 2050
    price_gz5 = 2050
    price_gz7 = 2050
    price_DGK = 1300
    price_NKTM = 2050
    price_NKTD = 2050
    price_NKTR = 2050
    price_ALPS = 1050
    value = depth_of_well * (price_ALPS + price_bk +
                             price_gz3 + price_gz1 + price_gz2 +
                             price_NKTD + price_gz4 +
                             price_gz5 + price_gz7 + price_DGK +
                             price_NKTM + price_NKTR)

    return value


def count_financial_model_reduced(depth_of_oil, depth_of_well):
    price_gz3 = 2050
    BK = 2450
    price_NKTD = 2050
    price_ALPS = 1050
    value = depth_of_well * (price_ALPS + price_gz3 + price_NKTD + BK)

    return value


def get_perc(number_of_well):
    global data
    df = data[data['well id']== int(number_of_well)]
    df = numpy.array(df.sort_values('depth, m')['goal'])
    return df


def get_data(wellid=None):
    global data
    idsss = get_perc(wellid)

    data_ = list()
    x = 0
    for i in idsss:
        x = x + 1
        if x % 2:
            continue
        data_.append(
            {
                "percent": int(i),
                "labs": [  # Исследования
                    {
                        "value": "A",
                    },
                    {
                        "value": "B",
                    },
                    {
                        "value": "C",
                    },
                ],
            }
        )

    data_1 = {
        "data": data_,
        "height": x
    }
    # data_1.update('data',  data_
    #               )
    #
    # data_1.update('height', x)

    h = round(find_depth_of_oil(data, wellid), 2)
    heigth = int(find_depth_of_well(data, wellid))

    porocity = 0.7
    S = 100
    ro = 860
    price_oil = 4.150
    cost = (S * ro * porocity * h * price_oil)
    exp_reduced = count_financial_model_reduced(h, heigth)
    exp_all = count_financial_model_all(h, heigth)

    searchs = {
        'data': [
            {
                'name': 'BK',
                'count': heigth,
                'cost': 2450,
                'y': heigth * 2450
            },
            {
                'name': 'GZ(1)',
                'count': heigth,
                'cost': 2050,
                'y': heigth * 2050
            },
            {
                'name': 'GZ(2)',
                'count': heigth,
                'cost': 2050,
                'y': heigth * 2050
            },
            {
                'name': 'GZ(3)',
                'count': heigth,
                'cost': 2050,
                'y': heigth * 2050
            },
            {
                'name': 'GZ(4)',
                'count': heigth,
                'cost': 2050,
                'y': heigth * 2050
            },
            {
                'name': 'GZ(5)',
                'count': heigth,
                'cost': 2050,
                'y': heigth * 2050
            },
            {
                'name': 'GZ(7)',
                'count': heigth,
                'cost': 2050,
                'y': heigth * 2050
            },
            {
                'name': 'DGK',
                'count': heigth,
                'cost': 1300,
                'y': heigth * 1300
            },
            {
                'name': 'NKTD',
                'count': heigth,
                'cost': 2050,
                'y': heigth * 2050
            },
            {
                'name': 'NKTM',
                'count': heigth,
                'cost': 2050,
                'y': heigth * 2050
            },
            {
                'name': 'NKTR',
                'count': heigth,
                'cost': 2050,
                'y': heigth * 2050
            },
            {
                'name': 'ALPS',
                'count': heigth,
                'cost': 1150,
                'y': heigth * 1150
            }
        ],
        # 'allSum': exp
    }

    return data_, searchs, cost, exp_reduced, exp_all, h, heigth, data_1


def index(request):
    well = 1
    global data
    ids = list( data['well id'].unique())

    if 'well' in request.GET and request.GET['well']:
        well = request.GET['well']

        data_, searchs, cost, exp_reduced, exp_all, h, heigth, idss = get_data(well)
        context = {
            'data': data_,
            'jsonSearch': json.dumps(searchs['data']),
            'searchs': searchs,
            'profitCost': '{0:,}'.format(int(cost)).replace(",", " "),
            'profitСostDollar': '{0:,}'.format(int(cost / 64)).replace(",", " "),
            'cost': '{0:,}'.format(int(cost - exp_reduced)).replace(",", " "),
            'costDollar': '{0:,}'.format(int((cost - exp_reduced) / 64)).replace(",", " "),
            'exp': '{0:,}'.format(int(exp_reduced)).replace(",", " "),
            'expAll': '{0:,}'.format(int(exp_all)).replace(",", " "),
            'expDollar': '{0:,}'.format(int(exp_reduced / 64)).replace(",", " "),
            'expDollarAll': '{0:,}'.format(int(exp_all / 64)).replace(",", " "),
            'height': heigth,
            'OilPrice': 4150,
            'type': 'SAND',
            'ids': ids,
            'h': h,
            'idss': json.dumps(idss),
        }
    else:
        return render_to_response('expert/index.html', {'ids': ids})  # Не обрабатываем
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
