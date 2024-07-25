from django.db import models


class Thing(models.Model):
    amount = models.IntegerField('Количество')
    name = models.CharField('Название', max_length=50, unique=True)
    class Meta:
        ordering = ['name']
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
