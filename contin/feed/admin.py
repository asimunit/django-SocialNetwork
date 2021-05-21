from django.contrib import admin
from .models import Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('description', 'date_posted', 'user_name')
    list_filter = ('user_name',)


admin.site.register(Post, PostAdmin)
