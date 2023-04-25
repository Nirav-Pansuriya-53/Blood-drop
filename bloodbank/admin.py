from django.contrib import admin
from bloodbank.models import BloodBank,CampSchedule, Donation, Request, Blood
from django.db.models import F
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Donation
from accounts_app.models import BloodGroup
from import_export.admin import ExportMixin, ImportMixin
from import_export import resources
from import_export import fields

@admin.register(BloodBank)
class AdminBloodBank(admin.ModelAdmin):
    list_display = ('email', 'phone_number',"iso_certified")
    search_fields = ('user_nameicontains', 'emailicontains', 'phone_number_icontains')
    list_filter = ('iso_certified',)

    def email(self, obj):
        return obj.user.email

    def phone_number(self, obj):
        return obj.user.phone_number


class BloodBankUserFilter(admin.SimpleListFilter):
    title = _('Blood Bank User')
    parameter_name = 'bloodbank_user'

    def lookups(self, request, model_admin):
        bloodbanks = model_admin.get_queryset(request).values_list('bloodbank_userid', 'bloodbankuser_name').distinct()
        return bloodbanks

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(bloodbank_user_id=self.value())
        else:
            return queryset
        
class BloodGroupFilter(admin.SimpleListFilter):
    title = 'Blood Group'

    parameter_name = 'blood_group'
    def lookups(self, request, model_admin):
        blood_groups = model_admin.get_queryset(request).values_list('donor_blood_group_blood_group', flat=True).distinct()
        return [(bg, bg) for bg in blood_groups if bg is not None]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(donor_blood_group_blood_group=self.value())
        else:                
            return queryset


class DonationResource(resources.ModelResource):
    donor_name = fields.Field(attribute='donor__name', column_name='Donor Name')
    bloodbank_name = fields.Field(attribute='bloodbank__user__name', column_name='Blood Bank Name')
    blood_group = fields.Field(attribute='donor__blood_group__blood_group', column_name='Blood Group')
    donation_date = fields.Field(attribute='donation_date', column_name='Donation Date')

    class Meta:
        model = Donation
        fields = ('donor_name', 'bloodbank_name', 'blood_group', 'donation_date')
        export_order = fields


@admin.register(Donation)
class DonationAdmin(ExportMixin, admin.ModelAdmin):
    list_display=("donor_name", "blood_bank_name", "blood_group", "donation_date")
    search_fields=("donor_name", )
    resource_class = DonationResource

    def donor_name(self, obj):
        return obj.donor.name

    def blood_bank_name(self, obj):
        return obj.bloodbank.user.name

    def blood_group(self, obj):
        return obj.donor.blood_group.blood_group if obj.donor.blood_group else None

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(donor_name=F("donor__name"))

    search_fields = ["donor__name", ]
    list_filter = ["donation_date", "bloodbank", "donor__blood_group__blood_group",]

    donor_name.short_description = "Donor"
    blood_bank_name.short_description = "Blood Bank "
    blood_group.short_description = "Blood Group"

    def blood_bank_name(self, obj):
        return obj.bloodbank.user.name
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(CampSchedule)
class CampScheduleAdmin(admin.ModelAdmin):
    list_display = ('bloodbank', 'date', 'starttime', 'endtime', 'address', 'pincode')
    # list_filter = (BloodBankUserFilter, 'date')
    search_fields = ('bloodbank_user_name', 'address')

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Request)
class CampScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'state', 'city')
    # list_filter = (BloodBankUserFilter, 'date')
    search_fields = ('city', 'state')

@admin.register(Blood)   
class BloodAdmin(ImportMixin,ExportMixin, admin.ModelAdmin):
    list_display = ("type","bloodbank")

    list_filter = ["bloodbank"]


