from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from coding.models import Tweet, Code, Category, Feature, UserProfile

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    inlines = [FeatureInline]

admin.site.register(Tweet)
admin.site.register(Code)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserProfileAdmin)
