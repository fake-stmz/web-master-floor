from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Product_Type(models.Model):
    """Тип продукции"""
    
    name = models.CharField(max_length=100)
    coefficient = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Material(models.Model):
    """Материал продукции"""
    
    material_type = models.CharField(max_length=100)
    defect_rate = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.material_type


class Product(models.Model):
    """Продукция"""
    
    name = models.CharField(max_length=100)
    article = models.IntegerField(unique=True)
    product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    minimal_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name


class Partner_Type(models.Model):
    """Тип партнера"""
    
    partner_type = models.CharField(max_length=100)

    def __str__(self):
        return self.partner_type


class Region(models.Model):
    """Регион"""
    
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    """Город"""
    
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Street(models.Model):
    """Улица"""
    
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Postal_Code(models.Model):
    """Почтовый индекс"""
    
    code = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.code)


class House(models.Model):
    """Дом"""
    
    number = models.CharField(max_length=10)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    postal_code = models.ForeignKey(Postal_Code, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.postal_code}, {self.street.city.region}, {self.street.city}, {self.street}, {self.number}"


class Partner(models.Model):
    """Партнер"""
    
    name = models.CharField(max_length=100)
    partner_type = models.ForeignKey(Partner_Type, on_delete=models.CASCADE)
    director = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.BigIntegerField()
    address = models.ForeignKey(House, on_delete=models.CASCADE)
    inn = models.BigIntegerField(unique=True)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    
    # Вычисление скидки
    def discount(self):
        sales_quantity = 0
        
        # Количество реализованной продукции
        for sale in Sale.objects.filter(partner=self.id):
            sales_quantity += sale.quantity
        
        # Рассчет скидки в зависимости от количества продаж
        if sales_quantity < 10000:
            return 0
        elif sales_quantity < 50000:
            return 5
        elif sales_quantity < 300000:
            return 10
        else:
            return 15
    
    def __str__(self):
        return self.name


class Sale(models.Model):
    """Продажа"""
    
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sale_date = models.DateField()
