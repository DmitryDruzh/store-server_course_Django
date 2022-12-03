from django.contrib import admin

from products.admin import BasketAdmin
from .models import User



# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)