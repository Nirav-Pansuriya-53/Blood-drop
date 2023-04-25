from django.contrib import admin
from django.conf import settings

class MyAdminSite(admin.AdminSite):
    # Set black as the default theme
    index_template = "admin/index_black.html"
    
admin_site = MyAdminSite(name='myadmin')
