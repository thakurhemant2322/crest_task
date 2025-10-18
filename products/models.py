from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)  # mandatory
    description = models.TextField()  # mandatory
    price = models.DecimalField(max_digits=10, decimal_places=2)  # mandatory
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # mandatory
    image = models.URLField()  # mandatory 
    ssn = models.CharField(max_length=32, unique=True)  # mandatory unique
    is_active = models.BooleanField()  # mandatory
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title


class ProductLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="logs")
    action = models.CharField(max_length=32)  # created / updated / disabled / deleted
    changes = models.JSONField(default=dict, blank=True)
    at = models.DateTimeField(auto_now_add=True)