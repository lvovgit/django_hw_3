from django.contrib import admin
from skychimp.models import Customer

# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)
    list_filter = ('name',)