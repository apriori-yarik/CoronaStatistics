from django.db import models
from django.urls import reverse

class Country(models.Model):
	name = models.CharField(max_length=50)
	flag_image = models.ImageField()
	map_image = models.ImageField()

	def get_absolute_url(self):
		return reverse('country', kwargs={'name': self.name})