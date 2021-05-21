from django.contrib import admin

# Register your models here.
from .models import Profile,Relationship


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'bio')
    list_filter = ('user',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Relationship)
