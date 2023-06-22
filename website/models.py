from django.db import models


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    passport_no = models.CharField(max_length=20, primary_key=True, null=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

