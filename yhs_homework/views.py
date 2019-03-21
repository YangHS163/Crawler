from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import os
import xlrd
# Create your views here.


def home(request):
    return render(request, 'cnn.html')


def tw(request):
    return render(request, 'twitter.html')


@csrf_exempt
def get_execl(request):
    if request.method == "POST":
        file_name = '/py/back/yhs_homework/' + request.POST['filename']
        # d = os.path.dirname(__file__) + '\\'
        # print(d)
        data = xlrd.open_workbook(file_name)
        if os.path.exists(file_name):
            data = xlrd.open_workbook(file_name)
            table = data.sheet_by_index(0)
            nrows = table.nrows
            execlData = []
            mytime = table.cell(1, 4).value
            print(mytime)
            for row in range(1, nrows):
                c = dict([('no', int(table.cell(row, 1).value)), ('href', table.cell(row, 2).value), ('heading', table.cell(row, 3).value)])
                execlData.append(c)
            return HttpResponse(json.dumps({
                "success": 1,
                "execlData": execlData,
                "time": mytime
            }))
        else:
            return HttpResponse(json.dumps({
                "success": -1
            }))

@csrf_exempt
def get_cnn(request):
    if request.method == "GET":
        output = os.popen("supervisorctl start Sel")
        p = output.read()
        if p.find('ERROR') == -1:
            flag = 1
        else:
            flag = -1
        return HttpResponse(json.dumps({
            "success": flag
        }))

    return HttpResponse(json.dumps({
        "success": 0
    }))



