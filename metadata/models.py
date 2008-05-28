from django.contrib.gis.db import models

class PointTestModel(models.Model):
    point = models.PointField()
    
    objects = models.GeoManager()
