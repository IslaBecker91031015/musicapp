# models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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
    experience = models.TextField(null=True, blank=True)
    instrument_avail = models.BooleanField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    instrument = models.ForeignKey('Instrument', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, primary_key=True)
    instruments = models.CharField(max_length=150, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('tutor_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name + ' - ' + self.instrument.name


class Student(models.Model):
    profile_pic = models.ImageField(upload_to="images/", default="concert.jpg") # pip3 install pillow
    extra_pic = models.ImageField(upload_to="images/", default="concert.jpg")
    name = models.CharField(max_length=150)
    about = models.TextField(null=True, blank=True)
    instrument_req = models.BooleanField(null=True, blank=True)
    instrument = models.ForeignKey('Instrument', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, primary_key=True)
    instruments = models.CharField(max_length=150, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name + ' - ' + self.instrument.name


## Booking System

class Hour(models.Model):
    hour = models.CharField(max_length=8)
    day_of_week = models.CharField(max_length=9)

    def __str__(self):
        return self.hour + ' - ' + self.day_of_week

class Availablity(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE)
    available = models.BooleanField(default=False)

    def __str__(self):
        if self.available:
            return self.tutor.name + ' on ' + self.hour.hour + ' ' \
                + self.hour.day_of_week + ' is available.'
        else:
            return self.tutor.name + ' on ' + self.hour.hour + ' ' + \
                self.hour.day_of_week + ' is booked'




class Booking(models.Model):
    availablity = models.ForeignKey(Availablity, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.name + ' booked ' + self.availablity.tutor.name + \
            ' on ' + self.availablity.hour.hour + ' ' + \
            self.availablity.hour.day_of_week
