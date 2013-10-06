from django.contrib import admin
from .models import Category, Product, OptionGroup, Option


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('path', 'name_path')
    list_display = ('name', 'is_active', 'path')
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(OptionGroup)
admin.site.register(Option)
