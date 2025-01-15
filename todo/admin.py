from django.contrib import admin
from .models import Task, Category

admin.site.register(Task)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)


# Register your models here.
