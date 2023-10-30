from django.db import models
from ckeditor.fields import RichTextField


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
        verbose_name_plural = 'Contact'
    

class Colors(BaseModel):
    color = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.color
    
    class Meta:
        verbose_name_plural = 'Colors'
    

class Categories(BaseModel):
    category = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.category
    
    class Meta:
        verbose_name_plural = 'Categories'
    

class Sizes(BaseModel):
    size = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.size
    
    class Meta:
        verbose_name_plural = 'Sizes'


class Clothes(BaseModel):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = RichTextField()
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    added_to_whishlist = models.BooleanField(default=False)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = f"{self.name.replace(' ', '-').lower()}-{str(self.create_time.strftime('%d-%m-%Y'))}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Clothes'
    

class Settings(BaseModel):
    facebook = models.URLField(max_length=50)
    instagram = models.URLField(max_length=50)
    pinterest = models.URLField(max_length=50)
    info = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'Settings'


class Logo(BaseModel):
    logo = models.ImageField(upload_to='media/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Logo'
    