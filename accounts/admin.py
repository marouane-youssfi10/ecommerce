from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account, AccountAdmin)

"""first_name = models.Ch
last_name = models.Cha
username = models.Char
email = models.EmailFi
phone_number = models.
# required
date_joined = models.D
last_login = models.Da
is_admin = models.Bool
is_staff = models.Bool
is_active = models.Boo
is_superadmin = models"""