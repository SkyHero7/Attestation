from django.db import models


class NetworkElement(models.Model):
    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='customers')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    level = models.IntegerField(choices=LEVEL_CHOICES, editable=False)

    def save(self, *args, **kwargs):
        if self.supplier is None:
            self.level = 0  # Завод
        elif self.supplier.level == 0:
            self.level = 1  # Розничная сеть
        elif self.supplier.level in [1, 2]:
            self.level = 2  # Индивидуальный предприниматель

        if self.debt is None:  # Проверяем, что debt не None
            self.debt = 0  # Устанавливаем debt на 0, если не задано другое значение

        super(NetworkElement, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()
    network_element = models.ForeignKey(NetworkElement, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
