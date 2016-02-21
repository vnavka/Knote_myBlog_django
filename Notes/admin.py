from django.contrib import admin
from Notes.models import KNote, Comments, UserImage

# Register your models here.
class NoteInline(admin.StackedInline):
    model = Comments
    extra = 0

class NoteAdmin(admin.ModelAdmin):
    fields = ['knote_title',
              'knote_note',
              'knote_date',
              'knote_host']
    inlines = [NoteInline]
    list_filter = ['knote_date','knote_title']

admin.site.register(KNote,NoteAdmin)
admin.site.register(Comments)
admin.site.register(UserImage)