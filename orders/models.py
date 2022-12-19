from django.db import models

from users.models import User

# Create your models here.


class Order(models.Model):

    CREATED = 0
    PAID = 1
    ON_WAY = 3
    DELIVERED = 4
    CHECKED = 5
    STATUSES = (
        (CREATED, 'создан'),
        (PAID, 'оплачен'),
        (ON_WAY, 'доставляется'),
        (DELIVERED, 'ждет в пункте выдачи'),
        (CHECKED, 'получен')
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    basket_history = models.JSONField(default=dict)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'order #{self.id} for {self.first_name} {self.last_name}'
