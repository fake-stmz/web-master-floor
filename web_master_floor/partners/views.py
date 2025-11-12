from django.shortcuts import render, redirect
from .models import *


def partner_list(request):
    
    partners = Partner.objects.all()
    
    return render(request, 'partner_list.html', { 'partners': partners })


def edit_partner(request, partner_id):
    
    partner = Partner.objects.get(id=partner_id)
    partner_types = Partner_Type.objects.all()
    
    if request.method == 'POST':
        create_or_update_partner(request, partner_id)
        
        return redirect('partner_list')
    
    return render(request, 'edit_add.html', { 'partner': partner, 'partner_types': partner_types })


def add_partner(request):
    
    partner_types = Partner_Type.objects.all()
    
    if request.method == 'POST':
        create_or_update_partner(request)
        
        return redirect('partner_list')
    
    return render(request, 'edit_add.html', { 'partner_types': partner_types })


def sales_history(request, partner_id):
    
    sales = Sale.objects.filter(partner=partner_id)
    partner_name = Partner.objects.get(id=partner_id).name
    
    return render(request, 'sales_history.html', { 'sales': sales, 'partner_name': partner_name })


def create_or_update_partner(request, partner_id=None):
    
    partner = None
    
    if partner_id:
        partner = Partner.objects.get(id=partner_id)
    else:
        partner = Partner()
    
    partner.name = request.POST.get('name')
    partner.director = request.POST.get('director')
    partner.email = request.POST.get('email')
    partner.phone = request.POST.get('phone')
    partner.inn = request.POST.get('inn')
    partner.rating = request.POST.get('rating')
        
    partner.partner_type = Partner_Type.objects.get(id=request.POST.get('type'))
        
    region = Region.objects.get_or_create(name=request.POST.get('region'))[0]
    city = City.objects.get_or_create(name=request.POST.get('city'), region=region)[0]
    street = Street.objects.get_or_create(name=request.POST.get('street'), city=city)[0]
    postal_code = Postal_Code.objects.get_or_create(code=request.POST.get('postal-code'))[0]
    house = House.objects.get_or_create(number=request.POST.get('house'), street=street, postal_code=postal_code)[0]
        
    partner.address = house
        
    partner.save()