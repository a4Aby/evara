from django.db import models

# Create your models here.

class razerPayAdmin(models.Model):
	company_id = models.CharField(max_length=200, null=True)
	razer_key = models.CharField(max_length=200, null=True)
	razer_secret = models.CharField(max_length=200)

	def __str__(self):
		return self.company_id
