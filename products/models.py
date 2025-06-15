from django.db import models

# Kategorije
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
# pod kategorije
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
#	 Proizvodi
class Products(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    subCategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brend = models.CharField(max_length=100, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    GENDR_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex'),
    )
    SIZE_CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
        ('XXXL', 'Triple Extra Large'),
        )
    
    gender = models.CharField(max_length=1, choices=GENDR_CHOICES, blank=True, default='U')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, null=True, default='M')

    # za prikaz slika
    def get_main_image(self):
        return self.images.filter(is_main=True).first()
    def __str__(self):
        return f"{self.name} - {self.category.name} - {self.subCategory.name}"
    

    


# Slike proizvoda
class ProductImage(models.Model):
    product = models.ForeignKey(Products, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)  # Označava glavnu sliku
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']

    def __str__(self):
     return f"{self.product.name} - {'Main' if self.is_main else 'Image'}"