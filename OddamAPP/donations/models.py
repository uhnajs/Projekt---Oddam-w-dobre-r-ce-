from django.db import models
from django.contrib.auth.models import User




class ExtendUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_user_verified = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Institution(models.Model):
    INSTITUTION_TYPE = (
        (1, "Charitable foundation"),
        (2, "Non-governmental organisation"),
        (3, "Local fund-raiser")
    )
    name = models.CharField(max_length=80)
    description = models.TextField()
    type = models.CharField(max_length=255, choices=INSTITUTION_TYPE)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.FloatField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=80)
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    is_taken = models.BooleanField(default=False)

    class Meta:
        ordering = ['pick_up_date', 'pick_up_time']

