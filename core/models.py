from django.db import models
from django.shortcuts import reverse

# Create your models here.
class song(models.Model):
    name = models.CharField(max_length = 200)
    artist = models.CharField(max_length = 200)
    lyrics = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.name)

class result(models.Model):
    name = models.CharField(max_length = 200)
    artist = models.CharField(max_length = 200)
    image = models.URLField()
    def __str__(self):
        return str(self.name)

    
