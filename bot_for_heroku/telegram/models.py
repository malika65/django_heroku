from django.db import models

class Oblasti(models.Model):
    name = models.CharField(max_length=200,verbose_name='Область',null=True,blank=True)
   
    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200,verbose_name='Область',null=True,blank=True)
    oblasti = models.ForeignKey(Oblasti, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
    
    def __str__(self):
        return self.name

    
class Raiony(models.Model):
    name = models.CharField(max_length=200,verbose_name='Район',null=True,blank=True)
    oblasti = models.ForeignKey(Oblasti, on_delete = models.CASCADE,related_name='oblasti')
    
    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'
    
    def __str__(self):
        return self.name

    
class Kenesh(models.Model):
    name = models.CharField(max_length=200,verbose_name='Кенеш',null=True,blank=True)
    raiony = models.ForeignKey(Raiony, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Кенеш'
        verbose_name_plural = 'Кенеши'

    def __str__(self):
        return self.name

    


