from django.db import models
import uuid

class People(models.Model):
    p_id = models.CharField(primary_key=True,unique=True, editable=True,max_length=50)
    name = models.CharField(max_length=200,verbose_name='ФИО',null=True)
    telephone = models.CharField(max_length=20,verbose_name='Номер телефона',null=True,blank=True)
    oblast = models.CharField(max_length=50,verbose_name='Область',null=True)
    raion = models.CharField(max_length=200,verbose_name='Район',null=True)
    doljnost = models.CharField(max_length=50,verbose_name='Должность',null=True)
    sale = models.BooleanField(default=False,verbose_name='Подтвержден админом')
    city = models.CharField(max_length=50,verbose_name='Город',null=True)
    kenesh = models.CharField(max_length=50,verbose_name='Кенеш',null=True)

    
    class Meta:
        verbose_name = 'Люди'
        verbose_name_plural = 'Люди'

    # def __unicode__(self):
    #     return self.name

    def __str__(self):
        return self.name
