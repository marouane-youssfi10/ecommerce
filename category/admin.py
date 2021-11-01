from django.contrib import admin
from .models import Category

# Register your models here.
"""
prepopulated_fields bach tgoul colone li dir 3lih slug dyana
"""
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin)
