from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name
