from django.db import models
from django.urls import reverse


# Създаване на модел за държавите, който ще се ползва от базата данни
class Country(models.Model):

	# Деклариране на свойствата на класа
	name = models.CharField(max_length=50)
	flag_image = models.ImageField()
	map_image = models.ImageField()

	def get_absolute_url(self):
		return reverse('country', kwargs={'name': self.name})