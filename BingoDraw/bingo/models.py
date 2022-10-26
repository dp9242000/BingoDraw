from django.db import models
from django.urls import reverse


# Create your models here.
class Card(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})


class Tile(models.Model):
    card = models.ForeignKey(Card, related_name='tiles', on_delete=models.CASCADE)
    tile_text = models.CharField(max_length=200)

    def __str__(self):
        return self.tile_text
