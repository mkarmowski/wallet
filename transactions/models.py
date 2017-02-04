import django.utils.timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db import models
from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule

from budgets.models import Budget, Saving

TRANSACTION_CHOICES = (
    ('income', 'Income'),
    ('expense', 'Expense'),
)


class Wallet(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, related_name='wallets')
    description = models.TextField(blank=True, null=True, max_length=500)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:wallet_details', args=[self.id])


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, related_name='categories')

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:category_details', args=[self.id])


class Transaction(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    type = models.CharField(choices=TRANSACTION_CHOICES, max_length=10)
    user = models.ForeignKey(User, related_name='transactions')
    wallet = models.ForeignKey(Wallet,
                               null=True,
                               blank=True,
                               related_name='transactions',
                               on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category,
                                 related_name='transactions',
                                 null=True,
                                 blank=True,
                                 on_delete=models.DO_NOTHING)
    budget = models.ForeignKey(Budget,
                               blank=True,
                               null=True,
                               default=None,
                               on_delete=models.DO_NOTHING)
    saving = models.ForeignKey(Saving,
                               blank=True,
                               null=True,
                               default=None,
                               on_delete=models.DO_NOTHING)
    date = models.DateField(verbose_name='Date of transaction',
                            default=django.utils.timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wallet:transaction_details', args=[self.id])

    def wallet_balance_adjust(self, wallet, transaction):
        if transaction.type == 'expense':
            wallet.balance -= transaction.amount
            return wallet.save()
        else:
            wallet.balance += transaction.amount
            return wallet.save()


# class TaskScheduler(models.Model):
#     periodic_task = models.ForeignKey(PeriodicTask)
#
#     @staticmethod
#     def schedule_every(task_name, minute=None, hour=None, day_of_week=None, day_of_month=None, month_of_year=None, args=None, kwargs=None):
#         # permissible_periods = ['days', 'hours', 'minutes', 'seconds']
#         # if period not in permissible_periods:
#         #     raise Exception('Invalid period specified')
#
#         # create periodic task and interval
#         ptask_name = '{}_{}'.format(task_name, datetime.now())
#         crontab_schedules = CrontabSchedule.objects.filter(minute=minute,
#                                                            hour=hour,
#                                                            day_of_week=day_of_week,
#                                                            day_of_month=day_of_month,
#                                                            month_of_year=month_of_year)
#         if crontab_schedules:
#             crontab_schedule = crontab_schedules[0]
#         else:
#             crontab_schedule = CrontabSchedule()
#             crontab_schedule.minute = minute
#             crontab_schedule.hour = hour
#             crontab_schedule.day_of_week = day_of_week
#             crontab_schedule.day_of_month = day_of_month
#             crontab_schedule.month_of_year = month_of_year
#             crontab_schedule.save()
#         ptask = PeriodicTask(name=ptask_name, task=task_name, crontab=crontab_schedule)
#         if args:
#             ptask.args = args
#         if kwargs:
#             ptask.kwargs = kwargs
#         ptask.save()
#         return TaskScheduler.objects.create(periodic_task=ptask)
#
#     def stop(self):
#         """pause the task"""
#         ptask = self.periodic_task
#         ptask.enabled = False
#         ptask.save()
#
#     def start(self):
#         """start the task"""
#         ptask = self.periodic_task
#         ptask.enabled = True
#         ptask.save()
#
#     def terminate(self):
#         self.stop()
#         ptask = self.periodic_task
#         self.delete()
#         ptask.delete()


class TaskScheduler(models.Model):
    periodic_task = models.ForeignKey(PeriodicTask)

    @staticmethod
    def schedule_every_month(task_name, minute, hour, day_of_month, args=None, kwargs=None):
        ptask_name = '{}_{}'.format(task_name, datetime.now())
        crontab_schedules = CrontabSchedule.objects.filter(minute=minute,
                                                           hour=hour,
                                                           day_of_month=day_of_month,)
        if crontab_schedules:
            crontab_schedule = crontab_schedules[0]
        else:
            crontab_schedule = CrontabSchedule()
            crontab_schedule.minute = minute
            crontab_schedule.hour = hour
            crontab_schedule.day_of_month = day_of_month
            crontab_schedule.save()
        ptask = PeriodicTask(name=ptask_name, task=task_name, crontab=crontab_schedule)
        if args:
            ptask.args = args
        if kwargs:
            ptask.kwargs = kwargs
        ptask.save()
        return TaskScheduler.objects.create(periodic_task=ptask)

    def stop(self):
        """pause the task"""
        ptask = self.periodic_task
        ptask.enabled = False
        ptask.save()

    def start(self):
        """start the task"""
        ptask = self.periodic_task
        ptask.enabled = True
        ptask.save()

    def terminate(self):
        self.stop()
        ptask = self.periodic_task
        self.delete()
        ptask.delete()
