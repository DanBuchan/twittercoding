from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from coding.models import Tweet, Code, Category, Feature, UserProfile

admin.site.unregister(User)
admin.site.unregister(Group)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 3
    fk_name = 'category'
    list_display = ('first_name', 'last_name')


class CategoryAdmin(admin.ModelAdmin):
    inlines = [FeatureInline]

admin.site.register(Tweet)
admin.site.register(Code)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserProfileAdmin)
