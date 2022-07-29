from django.contrib import admin
from coffeorders.models import *
# Register your models here.



class AccountAdmin(admin.ModelAdmin):
    list_display = ('email','firstname','lastname')
    search_fields = ('pk', 'email','firstname', 'lastname')
    readonly_fields=('pk', 'date_joined', 'last_login')

admin.site.register(Address)
admin.site.register(Customer,AccountAdmin)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
