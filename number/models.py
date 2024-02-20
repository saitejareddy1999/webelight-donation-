from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Number(models.Model):
    receiver_phone_number = models.CharField(max_length=11)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE'),
        (3, 'PENDING'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.IntegerField(choices=payment_status_choices, default=3)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_id and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('DONATE%Y%m%dODR') + str(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email + " " + str(self.id)
