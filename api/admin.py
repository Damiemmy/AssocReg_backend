from django.contrib import admin
from .models import Association,AssociationMembership,Transaction,Executive,Event,Receipt

# Register your models here.
admin.site.register(Association)
admin.site.register(AssociationMembership)
admin.site.register(Transaction)
admin.site.register(Executive)
admin.site.register(Event)
admin.site.register(Receipt)