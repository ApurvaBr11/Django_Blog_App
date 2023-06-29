from django.contrib import admin
from .models import *
# Register your models here.

class NotesAdmin(admin.ModelAdmin):
    list_display = ['id','user','content','date']
    list_filter = ['user','content']
    search_fields = ("user__username__icontains","content__icontains",'categories')


class NotesShearingAdmin(admin.ModelAdmin):
    list_display = ['id','notes','shared_by','shared_to']
    list_filter = ['notes','shared_by']

admin.site.register(Notes, NotesAdmin)
admin.site.register(Categories)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(NotesShearing,NotesShearingAdmin)
 

