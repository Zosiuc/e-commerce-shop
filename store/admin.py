from django.contrib import admin
from .models import Product, Category, Order, OrderItem, Banner
from django.utils.html import format_html

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','category', 'created_at', 'image_tag', 'new')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "-"

    image_tag.short_description = 'Image'


admin.site.site_header = "MyShop Admin"
admin.site.site_title = "MyShop Dashboard"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'paid']
    inlines = [OrderItemInline]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image', 'link']