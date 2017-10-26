import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import json
import nsepy as nsp

def index(request):
    data = nsp.get_history(symbol = trade_name, start = date.today(),end = date.today())
    return render(request, 'welcome/index.html', {
        'Closing': data.Close
    })


