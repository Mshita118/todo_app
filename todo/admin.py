from django.contrib import admin
from .models import Task, Category, Priority

admin.site.register(Task)
admin.site.register(Priority)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)


# Register your models here.
