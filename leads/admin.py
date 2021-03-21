from django.contrib import admin
from .models import Leads, Agent, User, Userprofile,Category
# Register your models here.

admin.site.register(Leads)
admin.site.register(Agent)
admin.site.register(User)
admin.site.register(Userprofile)
admin.site.register(Category)
