from django.shortcuts import render, redirect
from .models import *
from math import ceil


def partner_list(request):
    """Список партнеров"""
    
    # Все партнеры
    partners = Partner.objects.all()
    
    return render(request, 'partner_list.html', { 'partners': partners })


def edit_partner(request, partner_id):
    """Редактирование партнера"""
    
    # Если партнера с данным id не существует, перенаправляем на страницу добавления
    try:
        partner = Partner.objects.get(id=partner_id)
    except:
        return redirect('add_partner')
    
    # Все типы партнеров для выпадающего списка
    partner_types = Partner_Type.objects.all()
    
    # При отправке формы
    if request.method == 'POST':
        
        # Обновляем данные
        error = create_or_update_partner(request, partner_id)
        
        # Если возникла ошибка, выводим ее
        if error:
            return render(request, 'edit_add.html', { 'partner': partner, 'partner_types': partner_types, 'error': error })
        
        # Перенаправляем на список партнеров при успешном обновлении
        return redirect('partner_list')
    
    return render(request, 'edit_add.html', { 'partner': partner, 'partner_types': partner_types })


def add_partner(request):
    """Добавление партнера"""
    
    # Все типы партнеров для выпадающего списка
    partner_types = Partner_Type.objects.all()
    
    # При отправке формы
    if request.method == 'POST':
        
        # Добавляем партнера
        error = create_or_update_partner(request)
        
        # Если возникла ошибка, выводим ее
        if error:
            return render(request, 'edit_add.html', { 'partner_types': partner_types, 'error': error })
        
        # Перенаправляем на список партнеров при успешном добавлении
        return redirect('partner_list')
    
    return render(request, 'edit_add.html', { 'partner_types': partner_types })


def sales_history(request, partner_id):
    """История реализации продукции партнера"""
    
    # Все продажи партнера
    sales = Sale.objects.filter(partner=partner_id)
    
    # Имя партнера (чтобы вывести в заголовке)
    partner_name = Partner.objects.get(id=partner_id).name
    
    return render(request, 'sales_history.html', { 'sales': sales, 'partner_name': partner_name })


def material_count(request):
    """Тест метода расчета количества материала"""
    
    # При отправке формы
    if request.method == 'POST':
        
        # Получаем данные
        product_type_id = int(request.POST.get('type-id'))
        material_type_id = int(request.POST.get('material-type-id'))
        product_count = int(request.POST.get('count'))
        first_parameter = float(request.POST.get('first-param'))
        second_parameter = float(request.POST.get('second-param'))
        
        # Вызываем метод
        material_count = calculate_material_count(product_type_id, material_type_id, product_count, first_parameter, second_parameter)
        
        # Для удобства помещаем все в контекст
        context = {
            'product_type_id': product_type_id,
            'material_type_id': material_type_id,
            'product_count': product_count,
            'first_parameter': first_parameter,
            'second_parameter': second_parameter,
            'material_count': material_count
        }
        
        return render(request, 'material_count.html', context)
    
    return render(request, 'material_count.html')


def create_or_update_partner(request, partner_id=None):
    """Создание или обновление партнера"""
    
    try:
        partner = None
        
        # Если партнер с данным id существует - обновляем, в противном случае - создаем
        if partner_id:
            partner = Partner.objects.get(id=partner_id)
        else:
            partner = Partner()
        
        # Обновляем данные
        partner.name = request.POST.get('name')
        partner.director = request.POST.get('director')
        partner.email = request.POST.get('email')
        partner.phone = request.POST.get('phone')
        partner.inn = request.POST.get('inn')
        partner.rating = request.POST.get('rating')
        
        # Берем тип партнера из уже существующих
        partner.partner_type = Partner_Type.objects.get(id=request.POST.get('type'))
        
        # Создаем/получаем адрес (духота)
        region = Region.objects.get_or_create(name=request.POST.get('region'))[0]
        city = City.objects.get_or_create(name=request.POST.get('city'), region=region)[0]
        street = Street.objects.get_or_create(name=request.POST.get('street'), city=city)[0]
        postal_code = Postal_Code.objects.get_or_create(code=request.POST.get('postal-code'))[0]
        house = House.objects.get_or_create(number=request.POST.get('house'), street=street, postal_code=postal_code)[0]
        
        # Устанавливаем адрес
        partner.address = house

        # Сохраняем
        partner.save()
    except:
        # Если возникла ошибка, возвращаем ее
        return "Данные введены некорректно"
    
    return


def calculate_material_count(
        product_type_id: int, 
        material_type_id: int,
        product_count: int,
        first_parameter: float,
        second_parameter: float) -> int:
    """Метод расчета количества материала"""
    
    material_count = 0
    
    try:
        # Базовое вычисление
        material_count = product_count * first_parameter * second_parameter * float(Product_Type.objects.get(id=product_type_id).coefficient)
        
        # Учитываем коэффициент брака
        material_count = material_count / (1 - float(Material.objects.get(id=material_type_id).defect_rate))
    except:
        # Если возникла ошибка, возвращаем -1
        material_count = -1
    
    # Округляем до целого по высшему значению
    return ceil(material_count) if material_count > 0 else -1
