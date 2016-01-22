from django.contrib import admin
from coding.models import Tweet, Code, Category, Feature


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    inlines = [FeatureInline]

admin.site.register(Tweet)
admin.site.register(Code)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Feature)
# Register your models here.
