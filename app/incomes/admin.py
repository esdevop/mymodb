from django.contrib import admin
from .models import Income, IncomesGroup


admin.site.register(IncomesGroup)
admin.site.register(Income)
