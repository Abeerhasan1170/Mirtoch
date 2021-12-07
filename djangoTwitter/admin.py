from django.contrib import admin

from .models import Profile,Usernames,About,Publication,Volunteer, UserProfile, Country, Comment

admin.site.register(Profile),
admin.site.register(Usernames),
admin.site.register(About),
admin.site.register(Publication),
admin.site.register(Volunteer),
admin.site.register(UserProfile),
admin.site.register(Country),
admin.site.register(Comment),
# Register your models here.
