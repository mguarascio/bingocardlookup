from django.db import models

class BingoCard(models.Model):
	openid = models.CharField(max_length=200)
        grid   = models.CharField(max_length=300)

	def __unicode__(self):
		return self.grid
