from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from userprofile.models import Profile

# Unregister the User model
admin.site.unregister(User)

# Unregister the Group model
admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1

# Register your inline models

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]



    
admin.site.register(User, CustomUserAdmin)
