from django.contrib import admin

from .models import ActivationToken, PasswordResetToken, Profile


@admin.register(ActivationToken)
class ActivationTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth', 'info')
    list_filter = ('user', 'gender', 'date_of_birth')
    search_fields = ('user',)


