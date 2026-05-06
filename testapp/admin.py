from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import MyModel

class MyModelAdmin(admin.ModelAdmin):
    radio_fields = {'myfield': admin.VERTICAL}
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'myfield':
            kwargs['empty_label'] = "I WANT TO SET MY OWN EMPTY LABEL"
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Register the model admin
admin.site.register(MyModel, MyModelAdmin)
