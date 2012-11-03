from drmoon.models import UserProfile,NetworkGraph
from django.contrib import admin

admin.site.register(UserProfile)
admin.site.register(NetworkGraph)

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
	model = UserProfile
class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]
admin.site.register(User, UserProfileAdmin)
