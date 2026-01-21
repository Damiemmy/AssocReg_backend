# from django.contrib import admin
# from .models import User

# # Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['full_name', 'reg_number','email','phone']

# admin.site.register(User, UserAdmin)


from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'reg_number', 'email', 'phone', 'is_active')
    search_fields = ('full_name', 'reg_number', 'email')
    list_filter = ('is_active',)