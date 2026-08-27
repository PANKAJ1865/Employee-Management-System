from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.name} ({self.designation})"
