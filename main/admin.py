from django.contrib import admin

from main.models import NutritionalInfo
from .models import PieList, CarouselItems, Pies, FeaturedItems, PieHeaders, Allergens, BootstrapColours


@admin.register(PieList)
class PieListAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort_order', 'show_in_shop', 'cost', 'heading_text']
    list_editable = ['show_in_shop', 'cost', 'sort_order']


@admin.register(Allergens)
class AllergensAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(BootstrapColours)
class BootstrapColoursAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(CarouselItems)
class CarouselItemsAdmin(admin.ModelAdmin):
    list_display = ['heading_text', 'is_first', 'left_align', 'show_on_carousel', 'image_url', 'button_link']


@admin.register(FeaturedItems)
class FeaturedItemsAdmin(admin.ModelAdmin):
    list_display = ['heading_dark_text', 'heading_light_text', 'show_on_page', 'image_url']


@admin.register(PieHeaders)
class PieHeadersAdmin(admin.ModelAdmin):
    list_display = ['show_on_header']


@admin.register(NutritionalInfo)
class NutritionalInfoAdmin(admin.ModelAdmin):
    pass