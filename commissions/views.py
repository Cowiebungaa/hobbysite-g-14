from django.shortcuts import render
from .models import Commission

def commission_detail_1(request, pk):
    commission = Commission.objects.get(pk=pk)
    return render(request, 'commissions/commission_detail_1.html', {'commission': commission})

def commission_detail_2(request, pk):
    commission = Commission.objects.get(pk=pk)
    return render(request, 'commissions/commission_detail_2.html', {'commission': commission})

def commission_detail_3(request, pk):
    commission = Commission.objects.get(pk=pk)
    return render(request, 'commissions/commission_detail_3.html', {'commission': commission})

def commission_detail_4(request, pk):
    commission = Commission.objects.get(pk=pk)
    return render(request, 'commissions/commission_detail_4.html', {'commission': commission})

def commission_detail_5(request, pk):
    commission = Commission.objects.get(pk=pk)
    return render(request, 'commissions/commission_detail_5.html', {'commission': commission})
