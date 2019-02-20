# models.py
from django.db import models
from django.contrib.auth.models import User


class Instrument(models.Model):
    name = models.CharField(max_length=150)
    details = models.CharField(max_length=150, blank=True, null=True)

    # string displayed
    def __str__(self):
        return self.name


class Tutor(models.Model):
    profile_pic = models.ImageField(upload_to="images/", default="concert.jpg") # pip3 install pillow
    extra_pic = models.ImageField(upload_to="images/", default="concert.jpg")
    name = models.CharField(max_length=150)
    experience = models.TextField()
    instrument_avail = models.BooleanField()
    instrument = models.ForeignKey('Instrument', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, primary_key=True)

    def __str__(self):
        return self.name + ' - ' + self.instrument.name


class Student(models.Model):
    profile_pic = models.ImageField(upload_to="images/", default="concert.jpg") # pip3 install pillow
    extra_pic = models.ImageField(upload_to="images/", default="concert.jpg")
    name = models.CharField(max_length=150)
    instrument = models.CharField(max_length=150)
    about = models.TextField()
    instrument_req = models.BooleanField()
    instrument = models.ForeignKey('Instrument', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, primary_key=True)

    def __str__(self):
        return self.name + ' - ' + self.instrument.name
