from django.contrib import admin


# Register your models here.
from .models import Transaction_Owner,Store,Company,Bank_Account,Statement,Store_Transaction,Company_Transaction,Employee,Customer,Vendor,Organization

class StoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Store, StoreAdmin)




class CompanyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Company, CompanyAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Organization , OrganizationAdmin)


class Bank_AccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bank_Account, Bank_AccountAdmin)

class StatementAdmin(admin.ModelAdmin):
    list_display = ('working_date', 'store', 'writer','turnover', 'cash_money','bank_money','expenses')
    list_filter = ('working_date', 'store')
    fields = ['working_date', 'store', 'writer', ('turnover', 'cash_money','bank_money','expenses')]
admin.site.register(Statement, StatementAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('f_name', 'l_name')
    list_filter = ('f_name', 'l_name' )
    fields = ['f_name', 'l_name']
admin.site.register(Employee, EmployeeAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('f_name', 'l_name')
    list_filter = ('f_name', 'l_name' )
    fields = ['f_name', 'l_name']
admin.site.register(Customer, CustomerAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display = ('f_name', 'l_name')
    list_filter = ('f_name', 'l_name' )
    fields = ['f_name', 'l_name']
admin.site.register(Vendor, VendorAdmin)


class Company_TransactionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(Company_TransactionAdmin, self).get_queryset(request)
        qs = qs.select_related('transaction_owner__employee',
                               'transaction_owner__vendor',
                               'transaction_owner__customer')
        return qs

admin.site.register(Company_Transaction, Company_TransactionAdmin)

class Store_TransactionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(Store_TransactionAdmin, self).get_queryset(request)
        qs = qs.select_related('transaction_owner__employee',
                               'transaction_owner__vendor',
                               'transaction_owner__customer')
        # s = qs.select_related('transaction_owner')
        return qs

admin.site.register(Store_Transaction, Store_TransactionAdmin)
admin.site.register(Transaction_Owner)
