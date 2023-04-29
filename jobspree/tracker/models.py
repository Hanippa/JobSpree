from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
class Applying(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    company = models.CharField(max_length=50)
    keywords = models.CharField(max_length=50)
    priority = models.IntegerField(default=5,validators=[MaxValueValidator(10),MinValueValidator(0)])
    def __str__(self):
        return f'{self.user} | {self.company} | {self.keywords} | {self.priority}'
    

class Applied(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    company = models.CharField(max_length=50)
    date = models.DateField()
    result = models.CharField(max_length=50)
    score = models.IntegerField()
    def __str__(self):
        return f'{self.user} | {self.company} | {self.date} | {self.result} | {self.score}'

class Interviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    company = models.CharField(max_length=50)
    date = models.DateField()
    result = models.CharField(max_length=50)
    application = models.ForeignKey(Applied, on_delete= models.CASCADE)
    score = models.IntegerField()
    recording = models.FileField(blank=True , null=True , upload_to='static/media')
    def __str__(self):
        return f'{self.user} | {self.company} | {self.date} | {self.result} | {self.application} | {self.score}'