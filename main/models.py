from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qr_image = models.ImageField(upload_to='qr_codes', blank=True)

    def save(self, *args, **kwargs):
        qrcode_data = f"{self.name},{self.category},{self.price}"
        qrcode_img = qrcode.make(qrcode_data)
        canvas = BytesIO()
        qrcode_img.save(canvas, format='PNG')
        self.qr_image.save(f'qr_code_{self.pk}.png', File(canvas), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class Enter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} entered"



class Out(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} sold"




class Return(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} returned"
