from django.db import models


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
    

class Colors(BaseModel):
    color = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.color
    

class Categories(BaseModel):
    category = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.category
    

class Sizes(BaseModel):
    size = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.size


class Clothes(BaseModel):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='clothes', null=True, blank=True)
    added_to_whishlist = models.BooleanField(default=False)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    