from django.contrib import admin

# Register your models here.
from django.utils.translation import gettext_lazy as _ 
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin list view
    list_display = ("email", "first_name", "last_name", "birth_date", "phone_number", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    # Define the fieldsets for the add and change forms
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name", "birth_date", "phone_number", "profile_picture")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Define the fieldsets for the add form
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "birth_date", "phone_number", "profile_picture"),
        }),
    )

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)



from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "website", "location", "is_private", "created_at", "updated_at")
    list_filter = ("is_private", "location")
    search_fields = ("user__email", "website", "bio")
    readonly_fields = ("created_at", "updated_at")


from django.contrib import admin
from .models import Otp

@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ("user", "otp_code", "created_at", "expires_at", "is_expired")
    list_filter = ("created_at", "expires_at")
    search_fields = ("user__email", "otp_code")
    readonly_fields = ("created_at", "expires_at")    