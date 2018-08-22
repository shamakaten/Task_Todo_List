from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Company(models.Model):
    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компании'

    company_name = models.CharField('заголовок', max_length=120, unique=True)

    def __str__(self):
        return self.company_name


class Person(models.Model):
    class Meta:
        verbose_name = 'персонаж'
        verbose_name_plural = 'персонажи'

    user = models.ForeignKey(User, related_name='person', on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=400, verbose_name='Пароль')
    company = models.ManyToManyField(Company, verbose_name='Компании', blank=False)

    def __str__(self):
        return '{}, {}'.format(self.user.username, self.user.email)

    def get_company(self):
        return "\n".join([p.company_name for p in self.company.all()])

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)


class Todo(models.Model):
    class Meta:
        verbose_name = 'todo list'
        verbose_name_plural = 'todo lists'

    text = models.CharField(max_length=100)
    complete = models.BooleanField(default=False)
    company = models.ForeignKey(Company, verbose_name='Компания', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
