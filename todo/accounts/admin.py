from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AdminUser

from .models import Todo, User

@admin.register(User)
class Users(AdminUser):
    fieldsets = (
        (None, {"fields":("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name",)},),
        ("Permission", {"fields":("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},),
        ("Important date", {"fields": ("last_login", "date_joined")},),
    )
    
    add_fieldsets = (
        (None, {"classes":("wide",),"fields":("email", "password1", "password2"),},),
    )


    list_filter = ("is_staff", "is_superuser", "is_active")
    list_display_links = ("email",)
    list_display = ("email","is_staff" , "last_login",)
    search_fields = ("email", "first_name", "last_name", )
    ordering = ("email",)

@admin.register(Todo)
class TodosAdmin(admin.ModelAdmin):
    list_display = ("user","content", "is_complete", "timestamp")