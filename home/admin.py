from django.contrib import admin

# Register your models here.
from home.models import Setting, FAQ, ContactMessage

admin.site.register(Setting)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

admin.site.register(ContactMessage,ContactMessageAdmin)



class FAQAdmin(admin.ModelAdmin):
    list_display = ['question','status']
    list_filter = ['status']

admin.site.register(FAQ,FAQAdmin)