# UserType/admin.py
from django.contrib import admin
from .models import UserType

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    readonly_fields = ["id"]
    fields = ["id", "name"]