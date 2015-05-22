from django.contrib import admin
from .models import CustomBuild, PromoBox, GalleryPhoto


class GalleryAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)
    list_display = ('image_tag', 'title',)

admin.site.register(GalleryPhoto, GalleryAdmin)
admin.site.register(PromoBox)
admin.site.register(CustomBuild)