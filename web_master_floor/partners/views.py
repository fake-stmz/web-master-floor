from django.shortcuts import render
from .models import Partner


def partner_list(request):
    
    partners = Partner.objects.all()
    
    return render(request, 'partner_list.html', { 'partners': partners })