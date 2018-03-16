from django.contrib import admin
from serviceApp.models import userInf
from serviceApp.models import phonesInf
from serviceApp.models import workOrders
from serviceApp.models import gradesInf
from serviceApp.models import aboutInf

# Register your models here.
admin.site.register(userInf)
admin.site.register(phonesInf)
admin.site.register(workOrders)
admin.site.register(gradesInf)
admin.site.register(aboutInf)
