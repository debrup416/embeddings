from django.db import models


class Qa(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    question = models.TextField()
    answer= models.TextField(default="")
    
    class Meta:
        ordering = ['created']