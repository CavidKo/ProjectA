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
        
