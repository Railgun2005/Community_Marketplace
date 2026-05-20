from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Category,Item,Order,UserProfile

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'
    fields = ('phone','address','pan_number','gst_number','pfp','theme')

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)