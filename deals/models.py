from django.db import models


class Customer(models.Model):
    username = models.CharField(verbose_name="Имя", max_length=50, unique=True)
    spent_money = models.IntegerField(verbose_name="Сумма покупок", default=0)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-spent_money"]

    def get_gems(self):
        top_customers = Customer.objects.exclude(username=self)[:4]
        top_customers_gems = Gems.objects.filter(username__in=top_customers).values_list('gem', flat=True)
        gems_list = Gems.objects.filter(gem__in=top_customers_gems, username=self).values_list('gem', flat=True)
        return gems_list


class Gems(models.Model):
    gem = models.CharField(verbose_name="Название камня", max_length=50)
    username = models.ManyToManyField(Customer, blank=True)

    def __str__(self):
        return self.gem


class Deal(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Имя')
    item = models.CharField(verbose_name='Название товара', max_length=100)
    total = models.PositiveIntegerField('Сумма покупки')
    quantity = models.PositiveIntegerField('Количество товара')
    date = models.DateTimeField('Дата сделки')

    def __str__(self):
        return self.customer
