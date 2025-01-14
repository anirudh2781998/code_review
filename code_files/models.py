from django.db import models
from django.contrib.auth.models import  User
# Create your models here.
class CodeFile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    file=models.FileField(upload_to='code_files/')
    uploaded_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username}-{self.file.name}'