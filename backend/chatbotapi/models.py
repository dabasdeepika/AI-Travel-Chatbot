from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    price = models.IntegerField()
    category = models.CharField(max_length=20)  # budget, midrange, luxury

    def __str__(self):
        return f"{self.name} - {self.city}"

class Flight(models.Model):
    airline = models.CharField(max_length=50)
    departure = models.CharField(max_length=50)
    arrival = models.CharField(max_length=50)
    price = models.IntegerField()
    category = models.CharField(max_length=20)  # budget, midrange, luxury

    def __str__(self):
        return f"{self.airline} - {self.departure} to {self.arrival}"
