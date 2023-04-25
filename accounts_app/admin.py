from django.contrib import admin
from accounts_app.models import User,BloodGroup, BloodRequest
from django.contrib.auth.models import Group
from import_export.admin import ExportMixin
from import_export import resources
from import_export.fields import Field



class UserResource(resources.ModelResource):
    blood_group = Field(attribute='blood_group__blood_group')

    class Meta:
        model = User
        fields = ['name', 'email','blood_group', 'phone_number', 'age', 'weight']

@admin.register(User)
class AdminUser(ExportMixin, admin.ModelAdmin):
    resource_class = UserResource
    def get_blood_group(self, obj):
        return obj.group

    get_blood_group.short_description = 'Blood Group'
    list_display = ('name', 'email', 'get_blood_group', 'phone_number')
    list_filter = ('blood_group__blood_group',)
    search_fields = ("email","name")


class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(Group)