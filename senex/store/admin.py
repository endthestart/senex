from django.contrib import admin
from .models import Category, Product, OptionGroup, Option, OptionValue


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('path', 'name_path')
    list_display = ('name', 'is_active', 'path')
    prepopulated_fields = {"slug": ("name",)}


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class OptionInline(admin.TabularInline):
    model = OptionValue


class OptionAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline,
    ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OptionGroup)
admin.site.register(Option, OptionAdmin)
