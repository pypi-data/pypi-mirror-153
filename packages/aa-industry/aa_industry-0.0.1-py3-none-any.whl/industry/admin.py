from django.contrib import admin

from .models import UserToken, Facility


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'character_id', 'character_name', 'token']

    def character_name(self, obj):
        return obj.token.character_name


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'facility_id', 'facility_id', 'owner_id']
