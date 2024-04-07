from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserprofileModel

class ProfileuserInline(admin.StackedInline):
    model = UserprofileModel
    can_delete=False


class ExtendedUserAdmin(UserAdmin):
    inlines = [ProfileuserInline]

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)