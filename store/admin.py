from django.contrib import admin
from .models import Product
from django.utils.html import format_html


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "-"

    image_tag.short_description = 'Image'


admin.site.site_header = "MyShop Admin"
admin.site.site_title = "MyShop Dashboard"
# Register your models here.
