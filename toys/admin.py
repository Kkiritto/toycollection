from django.contrib import admin
from .models import Brand, Category, Toy, CollectionItem


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Toy)
class ToyAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'category', 'rarity', 'year', 'estimated_price')
    list_filter = ('rarity', 'brand', 'category', 'year')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(CollectionItem)
class CollectionItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'toy', 'personal_condition', 'purchase_price', 'added_at')
    list_filter = ('personal_condition',)
    search_fields = ('user__username', 'toy__title')