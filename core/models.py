from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from decimal import Decimal
from django.utils.translation import gettext_lazy as _


# Create your models here.
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contact(BaseModel):
    email = models.EmailField()
    message = models.TextField()

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name_plural = _('Contact')
        verbose_name = _('Contact')
    

class Colors(BaseModel):
    color = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.color
    
    class Meta:
        verbose_name_plural = _('Colors')
        verbose_name = _('Colors')
    

class Categories(BaseModel):
    category = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.category
    
    class Meta:
        verbose_name_plural = _('Categories')
        verbose_name = _('Categories')
    

class Sizes(BaseModel):
    size = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.size
    
    class Meta:
        verbose_name_plural = _('Sizes')
        verbose_name = _('Sizes')


class Tags(BaseModel):
    tag = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.tag
    
    class Meta:
        verbose_name_plural = _('Tags')
        verbose_name = _('Tags')


class Clothes(BaseModel):
    name = models.CharField(max_length=50)
    price = models.FloatField(null=True)
    description = RichTextField()
    image = models.ImageField(upload_to='media/product_images/', null=True, blank=True)
    added_to_whishlist = models.BooleanField(default=False)
    # color = models.ForeignKey(Colors, on_delete=models.CASCADE, null=True)
    # size = models.ForeignKey(Sizes, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    color = models.ManyToManyField(Colors)
    tag = models.ManyToManyField(Tags)
    size = models.ManyToManyField(Sizes)
    weight = models.CharField(max_length=10, null=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    width = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    materials = models.CharField(max_length=150, null=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)


    def save(self, *args, **kwargs):       
        if self.create_time is None:
            self.create_time = timezone.now()
        if self.slug is None:
            self.slug = f"{self.name.replace(' ', '-').lower()}-{str(self.create_time.strftime('%d-%m-%Y'))}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = _('Clothes')
        verbose_name = _('Clothes')


class CartProduct(BaseModel):
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True)
    size = models.CharField(max_length=10, null=True)
    color = models.CharField(max_length=10, null=True)
    active = models.BooleanField(default=True)
    overall_sum = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        self.overall_sum = round(int(self.quantity) * self.product.price, 2)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product.name
    
    class Meta:
        verbose_name_plural = _('Cart products')
        verbose_name = _('Cart products')
    

class Settings(BaseModel):
    adress = models.CharField(max_length=250, default=None)
    phone = models.CharField(max_length=20, default=None)
    support = models.EmailField(max_length=100, default=None)
    facebook = models.URLField(max_length=50)
    instagram = models.URLField(max_length=50)
    pinterest = models.URLField(max_length=50)
    info = models.CharField(max_length=500, null=True)

    class Meta:
        verbose_name_plural = _('Settings')
        verbose_name = _('Settings')


class Logo(BaseModel):
    logo = models.ImageField(upload_to='media/', null=True, blank=True)

    class Meta:
        verbose_name_plural = _('Logo')
        verbose_name = _('Logo')


class BlogCategories(BaseModel):
    category = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.category
    
    class Meta:
        verbose_name_plural = _('Blog categories')
        verbose_name = _('Blog categories')


class Blog(BaseModel):
    name = models.CharField(max_length=150, null=True)
    description = RichTextField()
    author = models.CharField(max_length=150, null=True)
    categories = models.ManyToManyField(BlogCategories)
    tags = models.ManyToManyField(Tags)
    comment_count = models.IntegerField(null=True)
    image = models.ImageField(upload_to='media/blog_images/', null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = _('Blogs')
        verbose_name = _('Blogs')