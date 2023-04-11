from django.db import models

class Data(models.Model):
    name = models.CharField(max_length=50)
    phones = models.IntegerField()
    date = models.DateTimeField()
    time = models.TimeField(auto_now=False, auto_now_add=False)

class Schedule(models.Model):
   
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    number_calls = models.IntegerField()
    retry_count = models.IntegerField()
    repeated_time = models.IntegerField()

class CallAnalitics(models.Model):
    name = models.CharField(max_length=50)
    phones = models.IntegerField()
    date = models.DateTimeField()
    time = models.TimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=20)