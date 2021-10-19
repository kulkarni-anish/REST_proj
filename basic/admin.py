from .forms import UserChangeForm, UserCreationForm
from django.contrib import admin
from .models import Journal, MyUser, Notes, ToDo, Workspace
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.



# class MyUserAdmin(admin.ModelAdmin):
#     #form = MyUserChangeForm
#     #add_form = MyUserCreationForm
    
#     model = MyUser
#     list_display = ['username', 'email', 'first_name','last_name'] 

#     search_fields = ['username','first_name','last_name']  

#     fieldsets = (
#         (None, {'fields': ('username','email', 'first_name', 'last_name','password','profile_picture')}),
#     )
#     add_fieldsets = (
#         (None, {'fields': ('username','email', 'first_name', 'last_name','password','profile_picture')}),
#     )

# admin.site.register(MyUserModel, MyUserAdmin)


class UserAdmin(BaseUserAdmin):
    
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

admin.site.register(ToDo)
admin.site.register(Workspace)
admin.site.register(Journal)
admin.site.register(Notes)