from django.db import models

class Size(models.Model):
    size = models.CharField(max_length=5)
    chest = models.IntegerField()
    brand_size = models.CharField(max_length=5)
    length = models.IntegerField()
    fit_preference = models.CharField(
        max_length=20,
        choices=[('slim', 'Slim'), ('avg', 'Average'), ('loose', 'Loose')],
            default='avg'  # Set a default value
    )


    def __str__(self):
        return f"{self.size} (Chest: {self.chest})"

class FemaleTopSize(models.Model):
    size = models.CharField(max_length=5)
    chest = models.IntegerField()
    brand_size = models.CharField(max_length=5)
    length = models.FloatField()
    sleeve_length = models.FloatField()
    fit_preference = models.CharField(
        max_length=20,
        choices=[('slim', 'Slim'), ('avg', 'Average'), ('loose', 'Loose')],
            default='avg'  # Set a default value
    )


class FemaleBottomSize(models.Model):
    size = models.CharField(max_length=5)
    waist = models.IntegerField()
    inseam_length = models.FloatField()
    brand_size = models.CharField(max_length=5)
    length = models.FloatField()
    hip = models.FloatField()
    fit_preference = models.CharField(
        max_length=20,
        choices=[('slim', 'Slim'), ('avg', 'Average'), ('loose', 'Loose')],
            default='avg'  # Set a default value
    )


class MaleTopSize(models.Model):
    size = models.CharField(max_length=5)
    chest = models.IntegerField()
    brand_size = models.CharField(max_length=5)
    length = models.FloatField()
    fit_preference = models.CharField(
        max_length=20,
        choices=[('slim', 'Slim'), ('avg', 'Average'), ('loose', 'Loose')],
            default='avg'  # Set a default value
    )


class MaleBottomSize(models.Model):
    size = models.CharField(max_length=5)
    waist = models.IntegerField()
    inseam_length = models.FloatField()
    brand_size = models.CharField(max_length=5)
    length = models.FloatField()
    hip = models.FloatField()
    rise = models.FloatField()
    fit_preference = models.CharField(
        max_length=20,
        choices=[('slim', 'Slim'), ('avg', 'Average'), ('loose', 'Loose')],
            default='avg'  # Set a default value
    )

