from django.contrib import admin
from .models import Car, UserProfile
from django.contrib import admin
from .models import User

# Register your models here.
admin.site.register(Car)
admin.site.register(User)

#Mix profile infor with user info 
class ProfileInLine(admin.StackedInline):
    model = UserProfile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["email","first_name","last_name"]
    inlines = [ProfileInLine]


admin.site.unregister(User)
admin.site.register(User,UserAdmin)

admin.site.register(UserProfile)





