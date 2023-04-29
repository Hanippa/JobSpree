from django.contrib import admin
from .models import Applying , Applied , Interviews

# Register your models here.
admin.site.register(Applying)
admin.site.register(Applied)
admin.site.register(Interviews)