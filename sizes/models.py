from django.db import models

class Size(models.Model):
    size = models.CharField(max_length=5)
    chest = models.IntegerField()
    brand_size = models.CharField(max_length=5)
    length = models.IntegerField()

    def __str__(self):
        return f"{self.size} (Chest: {self.chest})"

class FemaleTopSize(models.Model):
    size = models.CharField(max_length=5)
    chest = models.IntegerField()
    brand_size = models.CharField(max_length=5)
    length = models.FloatField()
    sleeve_length = models.FloatField()

class FemaleBottomSize(models.Model):
    size = models.CharField(max_length=5)
    waist = models.IntegerField()
    inseam_length = models.FloatField()
    brand_size = models.CharField(max_length=5)
    length = models.FloatField()
    hip = models.FloatField()

class MaleTopSize(models.Model):
    size = models.CharField(max_length=5)
    chest = models.IntegerField()
    brand_size = models.CharField(max_length=5)
    length = models.FloatField()

class MaleBottomSize(models.Model):
    size = models.CharField(max_length=5)
    waist = models.IntegerField()
    inseam_length = models.FloatField()
    brand_size = models.CharField(max_length=5)
    length = models.FloatField()
    hip = models.FloatField()
    rise = models.FloatField()
