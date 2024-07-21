from django.db import models


class NetworkElement(models.Model):
    """
    Модель элемента сети.

    Атрибуты:
        LEVEL_CHOICES (list): Список вариантов уровней для элемента сети.
        name (CharField): Название элемента сети.
        email (EmailField): Электронная почта элемента сети.
        country (CharField): Страна расположения элемента сети.
        city (CharField): Город расположения элемента сети.
        street (CharField): Улица расположения элемента сети.
        house_number (CharField): Номер дома элемента сети.
        created_at (DateTimeField): Дата и время создания элемента сети.
        supplier (ForeignKey): Связь с поставщиком (элементом сети).
        debt (DecimalField): Долг элемента сети.
        level (IntegerField): Уровень элемента сети.
    """
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
        """
        Сохранение элемента сети.

        Устанавливает уровень элемента сети в зависимости от его поставщика и
        устанавливает значение долга в 0, если оно не задано.

        Аргументы:
            *args: Неименованные аргументы.
            **kwargs: Именованные аргументы.
        """
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
        """
        Возвращает строковое представление элемента сети.

        Возвращает:
            str: Название элемента сети.
        """
        return self.name


class Product(models.Model):
    """
    Модель продукта.

    Атрибуты:
        name (CharField): Название продукта.
        model (CharField): Модель продукта.
        release_date (DateField): Дата выпуска продукта.
        network_element (ForeignKey): Связь с элементом сети, к которому относится продукт.
    """
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()
    network_element = models.ForeignKey(NetworkElement, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        """
        Возвращает строковое представление продукта.

        Возвращает:
            str: Название продукта.
        """
        return self.name


class Supplier(models.Model):
    """
    Модель поставщика.

    Атрибуты:
        name (CharField): Название поставщика.
        email (EmailField): Электронная почта поставщика.
        country (CharField): Страна расположения поставщика.
        city (CharField): Город расположения поставщика.
        street (CharField): Улица расположения поставщика.
        house_number (CharField): Номер дома поставщика.
        debt (DecimalField): Долг поставщика.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        """
        Возвращает строковое представление поставщика.

        Возвращает:
            str: Название поставщика.
        """
        return self.name
