from django.db import models

class NetworkElement(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=50)
    supplier = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='customers')
    debt = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()
    network_element = models.ForeignKey(NetworkElement, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
