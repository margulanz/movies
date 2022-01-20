from django.db import models

# Create your models here.

class movies(models.Model):
	id = models.AutoField(primary_key = True)
	original_title = models.CharField(max_length = 100)
	imdb_id = models.CharField(max_length = 10)
	overview = models.TextField()
	poster = models.TextField()