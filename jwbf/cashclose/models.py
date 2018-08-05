from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django_iban.fields import IBANField


from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


BANK_CHOICES = (
    ('NBG', 'Εθνική Τράπεζα'),
    ('Thessaly Bank', 'Συνεταιριστική Θεσσαλίας'),
    ('Alpha Bank', 'Αlpha Bank'),
    ('EuroBank', 'EuroBank'),
    ('Peiraeus Bank', 'Πειραιώς'),
)

class Bank_Account(models.Model):
    iban = IBANField()
    bank = models.CharField(max_length=15,choices=BANK_CHOICES)

    def get_absolute_url(self):
        return reverse('statement-detail', args=[str(self.iban)])

    def __str__(self):
        return f'{self.bank}, {self.iban}'

# Create your models here.
class Store(models.Model):
    store= models.CharField(max_length=15, help_text="Enter a store)" ,  primary_key=True)
    address = models.CharField(max_length=50, help_text="Enter a store address")
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=False)
    def __str__(self):
        return self.store

    def get_absolute_url(self):
        return reverse('store-detail', args=[str(self.store)])

class Company(models.Model):
    display_name = models.CharField(max_length=150, help_text="Company's name that you communicate")
    legal_name = models.CharField(max_length=150,help_text="Company's official name")
    bank = models.ForeignKey('Bank_Account', on_delete=models.CASCADE, null=False)
    organization= models.ForeignKey('Organization', on_delete=models.CASCADE, null=False)

    class Meta:
        pass

    def __str__(self):
        return self.legal_name

    def get_absolute_url(self):
        return reverse('company-detail', args=[self.pk])

class Organization(models.Model):
    name = models.CharField(max_length=150, help_text="Company's name that you communicate")
    class Meta:
        pass

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organization-detail', args=[self.pk])

class Statement(models.Model):
    working_date = models.DateField(null=False,blank=False)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, null=False)
    turnover = models.DecimalField(max_digits=10, default=0, decimal_places=2,help_text="Enter Turnover")
    cash_money = models.DecimalField(max_digits=10, default=0, decimal_places=2,help_text="Enter Cash")
    bank_money = models.DecimalField(max_digits=10, default=0, decimal_places=2, help_text="Enter cards ")
    expenses = models.DecimalField(max_digits=10, default=0, decimal_places=2, help_text="Enter Expenses")
    writer = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)

    def save_model(self, request, obj, form, change):
        obj.writer = request.user
        super().save_model(request, obj, form, change)

    @property
    def is_overdue(self):
        if self.working_date and date.today() > self.working_date:
            return True
        return False

    class Meta:
        unique_together = (('working_date', 'store'),)

    def get_absolute_url(self):
        return reverse('statement-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.working_date}, {self.store}'

class Transaction_Owner(models.Model):

    def __str__(self):
        return "Transaction_Owner: {0}".format(repr(self.target))

    @property
    def target(self):
        if getattr(self, 'customer', None) is not None:
            return self.customer
        if getattr(self, 'Vendor', None) is not None:
            return self.vendor
        if getattr(self, 'employee', None) is not None:
            return self.employee
        return None


class Employee(Transaction_Owner):
    f_name =  models.CharField(max_length=40, help_text="Enter a first name)")
    l_name =  models.CharField(max_length=40, help_text="Enter a last name)")

    def __str__(self):
        return self.l_name


class Vendor(Transaction_Owner):
    f_name =  models.CharField(max_length=40, help_text="Enter a first name)")
    l_name =  models.CharField(max_length=40, help_text="Enter a last name)")

    def __str__(self):
        return self.l_name


class Customer(Transaction_Owner):
    f_name =  models.CharField(max_length=40, help_text="Enter a first name)")
    l_name =  models.CharField(max_length=40, help_text="Enter a last name)")

    def __str__(self):
        return self.l_name



class Store_Transaction(models.Model):
    transaction_owner = models.ForeignKey(Transaction_Owner, on_delete=models.CASCADE)
    transaction_date= models.DateField(default=date.today)
    submitted_date= models.DateField(default=date.today)
    submitted_by=models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=200)
    netvalue = models.DecimalField(max_digits=10, default=0, decimal_places=2, help_text="Enter value")

    def __str__(self):
        return "{0}, owned by {1}".format(self.description, repr(self.transaction_owner.target))


class Company_Transaction(models.Model):
    transaction_owner = models.ForeignKey(Transaction_Owner, on_delete=models.CASCADE)
    transaction_date = models.DateField(default=date.today)
    submitted_date = models.DateField(default=date.today)
    submitted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=200)
    netvalue = models.DecimalField(max_digits=10, default=0, decimal_places=2, help_text="Enter value")

    def __str__(self):
        return "{0}, owned by {1}".format(self.description, repr(self.transaction_owner.target))