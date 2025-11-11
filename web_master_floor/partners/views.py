from django.shortcuts import render
from .models import Partner


def partner_list(request):
    
    partners = Partner.objects.all()
    
    return render(request, 'partner_list.html', { 'partners': partners })

def edit_partner(request, partner_id):
    
    partner = Partner.objects.get(id=partner_id)
    
    return render(request, 'edit_add.html', { 'partner': partner })

def add_partner(request):
    
    return render(request, 'edit_add.html')